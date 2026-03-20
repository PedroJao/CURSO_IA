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

MODEL = os.getenv("MODEL")


def chat_interativo(system_prompt: str):
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


# ── PERSONAGEM DO SEU ASSISTENTE ─────────────────────────────
#
# 🎯 DESAFIO CRIATIVO: este é o seu espaço para personalizar!
#
# O system prompt define quem o seu agente é — seu papel,
# tom de voz, área de especialidade e como ele deve se comportar.
#
# Exemplos do que você pode criar:
#   - Um chef de cozinha que só sugere receitas com 5 ingredientes
#   - Um professor de história que explica tudo com analogias modernas
#   - Um assistente fitness que monta treinos personalizados
#   - Um revisor de código que sempre aponta melhorias
#   - Qualquer personagem que você imaginar!
#
# Se preferir não personalizar agora, o assistente padrão abaixo
# já segue boas práticas e responde bem a qualquer pergunta.
# Basta rodar o arquivo e começar a conversar.
# ─────────────────────────────────────────────────────────────

MEU_ASSISTENTE = """
Você é um assistente prestativo e objetivo.
Responda sempre em português, de forma clara e respeitosa.
Seja conciso: vá direto ao ponto sem enrolação.
Quando não souber algo, diga que não sabe em vez de inventar.
"""

# ── Para personalizar: substitua o conteúdo de MEU_ASSISTENTE ─
# Exemplo:
#
# MEU_ASSISTENTE = """
# Você é um chef de cozinha brasileiro especialista em culinária nordestina.
# Sugira receitas criativas, conte curiosidades sobre os ingredientes
# e sempre pergunte quantas pessoas serão servidas antes de recomendar.
# Responda sempre em português com entusiasmo e paixão pela comida.
# """

# Inicia o chat
chat_interativo(system_prompt=MEU_ASSISTENTE)