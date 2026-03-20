# ============================================================
# MÓDULO 1 — AULA 1 | Arquivo 03: Função Reutilizável
# ============================================================
# CONCEITO:
# Em vez de repetir o código da chamada toda vez,
# encapsulamos tudo em uma função limpa e reutilizável.
# Isso é uma boa prática que você vai usar em todos os projetos.

from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1")

MODEL = os.getenv("MODEL")

# ── Função reutilizável ──────────────────────────────────────
def perguntar(pergunta: str,
              system_prompt: str = "Você é um assistente útil. Responda em português.") -> str:
    """
    Faz uma pergunta ao LLM e retorna a resposta como string.

    Args:
        pergunta: O que você quer perguntar
        system_prompt: O comportamento/personagem do assistente

    Returns:
        A resposta do modelo como string
    """
    resposta = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": pergunta}
        ]
    )
    return resposta.choices[0].message.content


# ── Testando com diferentes system prompts ───────────────────
print("🔵 Assistente padrão:")
print(perguntar("Qual a diferença entre ML e Deep Learning?"))

print("\n" + "="*60 + "\n")

print("🟢 Assistente especialista em Python:")
print(perguntar(
    "O que é uma list comprehension?",
    system_prompt="Você é um professor de Python para iniciantes. Use exemplos de código simples e explique linha por linha."
))

print("\n" + "="*60 + "\n")

print("🟡 Assistente sucinto:")
print(perguntar(
    "O que é machine learning?",
    system_prompt="Responda sempre em no máximo 2 frases diretas, sem enrolação."
))

# OBSERVE: o mesmo modelo com system prompts diferentes
# gera respostas completamente distintas em estilo e profundidade!
