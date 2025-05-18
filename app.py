
import os
import re
import requests
import gradio as gr
from datetime import datetime
from urllib.parse import quote

# 🔐 API Gemini via ambiente
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
    "Você é um chef prático, direto e simpático, com linguagem acessível e foco em economia e aproveitamento.\n"
    "Regras importantes:\n"
    "- Use no máximo 4 ingredientes por receita. Sal, pimenta-do-reino e azeite são curingas e não contam.\n"
    "- Nunca use todos os ingredientes se houver mais de 5; divida e crie até 3 receitas simples e distintas.\n"
    "- Fale com clareza. Evite termos técnicos ou linguagem infantilizada.\n"
    "- Utilize medidas práticas: colheres, xícaras, unidades, gramas, kg, ml ou litros — escolha conforme o alimento.\n"
    "- Dê dicas rápidas de conservação (ex: como armazenar, congelar ou reaproveitar).\n"
    "- Sempre que possível, sugira uso integral (cascas, talos, sobras) ou alternativas econômicas.\n"
    "- Se algum ingrediente tiver validade informada, mencione quanto tempo falta e priorize seu uso.\n"
    "- Evite exageros ou receitas muito elaboradas. O foco é praticidade com o que já se tem.\n"
    "- Responda de forma organizada, com nome da receita, ingredientes e instruções simples.\n"
    "- Verifique a data de validade do produto se for menor que à data atual, não gere receita e sugira o descarte.\n"
    "- Seja gentil, mas objetivo. O usuário busca praticidade e ideias realistas para o dia a dia.\n"
    f"\nIngredientes fornecidos: {texto_usuario}\n"
    "Responda com simpatia, clareza e foco na utilidade."
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
            texto_resposta += f"\n\n📅 [Agendar lembrete de uso de {alimento} no Google Calendar]({link})"

    return texto_resposta

# Interface com correções visuais
with gr.Blocks(css="""
body {
    background: linear-gradient(135deg, #000000, #1c1c1c, #333333);
    color: #f1f1f1;
    font-family: 'Inter', sans-serif;
}
.container {
    max-width: 720px;
    margin: auto;
    padding: 24px;
    background-color: #222222e6;
    border-radius: 16px;
    box-shadow: 0 0 12px #00000044;
}
#titulo {
    font-size: 26px;
    font-weight: 600;
    text-align: center;
    margin-bottom: 12px;
    color: #f0f0f0;
}
#entrada {
    border-radius: 6px;
}
#botao {
    font-size: 16px;
    margin-top: 12px;
    padding: 10px 20px;
    background-color: #2196f3;
    color: white;
    border: none;
    border-radius: 6px;
    width: 100%;
}
.output-markdown {
    background-color: #ffffff10;
    border-radius: 10px;
    padding: 16px;
    margin-top: 20px;
    color: #fff;
}
img.avatar {
    display: block;
    margin: auto;
    width: 120px;
}
@media(max-width: 600px) {
    .container {
        padding: 16px;
        margin: 12px;
    }
    #titulo {
        font-size: 20px;
    }
}
""") as demo:

    gr.HTML("<style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');</style>")

    with gr.Column(elem_classes="container"):
        gr.Image(value="static_chefia.png", show_label=False, elem_id="avatar", elem_classes="avatar")
        gr.Markdown("### 👩‍🍳 **ChefIA – Assistente de Cozinha Inteligente**", elem_id="titulo")
        entrada = gr.Textbox(label="Digite algo que você tenha na geladeira ou no armário e descubra receitas, dicas de aproveitamento e até agende um alerta para descartar na validade, só inserir a data!", placeholder="Ex: Arroz cozido de ontem, peito de frango, legumes na gaveta, creme de leite – vence dia 20/09...", lines=2, elem_id="entrada")
        botao = gr.Button("🍽️ Gerar Receita", elem_id="botao")
        saida = gr.Markdown(elem_classes=["output-markdown"])

        botao.click(fn=responder_chefia, inputs=entrada, outputs=saida)

if __name__ == "__main__":
    demo.launch()
