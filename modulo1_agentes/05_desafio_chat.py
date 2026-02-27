# ============================================================
# MÓDULO 1 — AULA 1 | Arquivo 05: Desafio — Chat Interativo
# ============================================================
# DESAFIO:
# Um loop de conversa no terminal onde você digita mensagens
# e o modelo responde, mantendo o contexto da conversa.
# Digite "sair" para encerrar.
#
# Este é o projeto final da Semana 4 do Módulo 1!

from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1")

MODEL = "openrouter/auto"


def chat_interativo(system_prompt: str = "Você é um assistente amigável. Responda em português."):
    """
    Loop interativo de conversa com memória completa.
    Digite 'sair' para encerrar, 'limpar' para resetar o histórico.
    """
    historico = [{"role": "system", "content": system_prompt}]

    print("=" * 55)
    print("  💬 Chat com IA — digite 'sair' para encerrar")
    print("                   digite 'limpar' para novo chat")
    print("=" * 55 + "\n")

    while True:
        entrada = input("Você: ").strip()

        if not entrada:
            continue

        if entrada.lower() == "sair":
            print("\n👋 Até a próxima aula!")
            break

        if entrada.lower() == "limpar":
            historico = [{"role": "system", "content": system_prompt}]
            print("🗑️  Histórico limpo! Nova conversa iniciada.\n")
            continue

        # Adiciona ao histórico e envia tudo ao modelo
        historico.append({"role": "user", "content": entrada})

        try:
            resposta = client.chat.completions.create(
                model=MODEL,
                messages=historico
            )
            resposta_texto = resposta.choices[0].message.content
            historico.append({"role": "assistant", "content": resposta_texto})

            print(f"\n🤖 IA: {resposta_texto}\n")

        except Exception as e:
            print(f"\n❌ Erro na chamada: {e}")
            print("Verifique sua chave de API e conexão.\n")
            historico.pop()  # remove a mensagem que falhou


# ── Escolha o personagem do seu assistente ───────────────────
MEU_ASSISTENTE = """
Você é um tutor de Inteligência Artificial especializado em Python.
Seu estilo é didático, paciente e usa exemplos práticos de código.
Quando der exemplos de código, use blocos ```python```.
Responda sempre em português.
"""

# Inicia o chat
chat_interativo(system_prompt=MEU_ASSISTENTE)