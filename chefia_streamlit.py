import os
import re
import requests
import streamlit as st
from datetime import datetime
from urllib.parse import quote

# 🔐 Carrega a chave da API do ambiente
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"

def gerar_link_google_calendar(nome_alimento, data_validade, hora="08:00"):
    try:
        data = datetime.strptime(data_validade, "%Y-%m-%d")
        inicio = data.strftime("%Y%m%dT") + hora.replace(":", "") + "00"
        fim = data.strftime("%Y%m%dT") + str(int(hora[:2]) + 1).zfill(2) + hora[2:] + "00"
        titulo = f"Usar {nome_alimento} antes de vencer"
        return (
            f"https://calendar.google.com/calendar/render?action=TEMPLATE"
            f"&text={quote(titulo)}&dates={inicio}/{fim}"
            f"&details={quote('Lembrete criado com ChefIA')}"
        )
    except Exception:
        return None

def extrair_validade(texto):
    match = re.search(r'(\b\w+).*?venc[ea]?.*?(\d{1,2}[/-]\d{1,2}[/-]?[\d{0,4}])', texto.lower())
    if match:
        alimento = match.group(1)
        data = match.group(2).replace("-", "/")
        partes = data.split("/")
        if len(partes) != 3:
            return None, None
        if len(partes[2]) == 2:
            partes[2] = "20" + partes[2]
        try:
            data_formatada = f"{partes[2]}-{int(partes[1]):02d}-{int(partes[0]):02d}"
            return alimento, data_formatada
        except:
            return None, None
    return None, None

def gerar_prompt(texto_usuario):
    return (
        "Você é um chef prático, direto e simpático, com linguagem acessível e foco em economia e reaproveitamento.\n"
        "Regras importantes:\n"
        "- Use no máximo 4 ingredientes por receita. Sal, pimenta-do-reino e azeite são curingas.\n"
        "- Divida ingredientes se houver muitos e crie até 3 receitas simples.\n"
        "- Utilize medidas práticas.\n"
        "- Dê dicas de conservação e reaproveitamento.\n"
        "- Priorize itens com validade próxima.\n"
        "- Responda de forma clara, organizada e simpática.\n"
        f"\nIngredientes fornecidos: {texto_usuario}\n"
        "Responda com simpatia e foco na utilidade."
    )

def responder_chefia(texto_usuario):
    prompt = gerar_prompt(texto_usuario)
    resposta = requests.post(
        GEMINI_URL,
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )

    if resposta.status_code != 200:
        return "⚠️ Erro ao acessar a API. Verifique sua chave."

    conteudo = resposta.json()
    texto_resposta = conteudo["candidates"][0]["content"]["parts"][0]["text"]

    alimento, data = extrair_validade(texto_usuario)
    if alimento and data:
        link = gerar_link_google_calendar(alimento, data)
        if link:
            texto_resposta += f"\n\n📅 [Agendar lembrete para {alimento}]({link})"

    return texto_resposta

# Interface com Streamlit
st.set_page_config(page_title="ChefIA", layout="centered")
st.title("👩‍🍳 ChefIA – Assistente de Cozinha com IA")

user_input = st.text_area("Digite ingredientes ou algo com validade:", height=100, placeholder="Ex: arroz, cenoura, frango vence 25/06...")

if st.button("🍽️ Gerar Receita"):
    if not user_input.strip():
        st.warning("Digite pelo menos um ingrediente.")
    else:
        resposta = responder_chefia(user_input)
        st.markdown(resposta, unsafe_allow_html=True)