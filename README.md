# 👩‍🍳 ChefIA – Assistente de Cozinha Inteligente

O **ChefIA** é um chatbot interativo que funciona como um assistente culinário direto e prático. Ele ajuda a evitar desperdícios, aproveita ingredientes que você já tem e sugere receitas simples com base no que está disponível — inclusive com lembretes automáticos de validade.

🧠 Desenvolvido com foco em **utilidade, reaproveitamento e praticidade**, durante a **Imersão IA 2025** da Alura com o Google.

---

## 🔧 Funcionalidades

- 🍽️ Sugestão de receitas com no máximo 4 ingredientes principais
- 🧠 Geração de respostas via **Google Gemini API**
- 🥕 Dicas de conservação e reaproveitamento (talos, cascas, sobras)
- 📅 Detecta automaticamente alimentos com validade informada e gera **link de agendamento no Google Calendar**
- 🔄 Interface com **Gradio**, responsiva e fácil de usar
- 🚫 Botão de encerramento da conversa
- ✅ Roda direto no navegador, via **Google Colab** ou servidor próprio

---

## 💻 Como Usar

1. **Configure a variável `GOOGLE_API_KEY`** no ambiente (não coloque a chave diretamente no código)
2. Suba o projeto localmente ou rode via Colab
3. Digite ingredientes ou mensagens como:
   - `banana, aveia e mel`
   - `frango vence 25/05/2025`
4. O ChefIA analisará sua mensagem e:
   - Gerará sugestões culinárias com base em até 4 ingredientes
   - Dará dicas de armazenamento e reaproveitamento
   - Criará um link para adicionar lembrete no Google Calendar, caso detecte validade

---

## 🖼️ Interface

A interface do projeto é responsiva e moderna, com:
- Estilo escuro
- Tipografia legível (Fonte: Inter)
- Avatar personalizado
- Layout com destaque para simplicidade e acessibilidade

---

## 🧪 Exemplo de Uso

```
🧑 Você: cenoura, cebola e ovo

🤖 ChefIA:
🥕 Omelete de Cenoura Ralada
Ingredientes:
- 2 ovos
- 1/2 cenoura ralada
- 1/4 de cebola picada

Modo de preparo:
Bata os ovos, junte os ingredientes e frite em frigideira antiaderente.

Dica: armazene a cenoura em pote vedado com papel toalha para maior durabilidade.
```

---

## 📁 Estrutura do Projeto

```
📦 chefia/
├── app.py           → App principal com Gradio e Gemini API
├── static_chefia.png → Imagem do avatar do assistente
├── README.md        → Este arquivo
```

---

## 🚀 Tecnologias Utilizadas

- Python 3
- Gradio
- Google Gemini API (via `generativelanguage.googleapis.com`)
- Google Calendar (via links públicos)
- Regex e datetime para análise semântica de texto

---

## ⚠️ Observações

- Gratuito para uso com **sua própria API Key do Google Gemini**
- A integração com o Google Calendar é feita por link público, sem acesso direto à sua conta
- Nenhuma informação do usuário é armazenada

---

## 👨‍💻 Criado por

**Tiago Rodrigues**  
Nutricionista | Desenvolvedor Front-End em formação | Criador do ChefIA  
🔗 [LinkedIn](https://www.linkedin.com/in/000tiago)  
🔗 [GitHub](https://github.com/000tiago)
