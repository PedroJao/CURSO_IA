# ============================================================
# MÓDULO 1 — AULA 1 | Arquivo 02: Primeira Chamada à API
# ============================================================
# CONCEITO:
# A API de chat funciona com uma lista de "mensagens".
# Cada mensagem tem um "role" e um "content".
#
# Roles:
#   "system"    → instrução de comportamento (o "personagem" do modelo)
#   "user"      → o que você escreve
#   "assistant" → o que o modelo responde

from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1")

MODEL = "openrouter/auto"

# ── Fazendo a primeira chamada ───────────────────────────────
resposta = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": "Você é um assistente educacional especialista em Python e IA. Responda sempre em português, de forma clara e didática."
        },
        {
            "role": "user",
            "content": "O que é um agente de IA? Explique em 3 linhas."
        }
    ]
)

# Extraindo o texto da resposta
texto = resposta.choices[0].message.content
print("🤖 Resposta do modelo:")
print(texto)

# ── Explorando o objeto de resposta ─────────────────────────
# A resposta contém muito mais do que só o texto!
print("\n📊 Informações da chamada:")
print(f"  Modelo usado:     {resposta.model}")
print(f"  Tokens de input:  {resposta.usage.prompt_tokens}")
print(f"  Tokens de output: {resposta.usage.completion_tokens}")
print(f"  Total de tokens:  {resposta.usage.total_tokens}")

# IMPORTANTE: tokens = custo.
# Regra geral: 1 token ≈ 0.75 palavras em inglês / ≈ 0.5 em português
