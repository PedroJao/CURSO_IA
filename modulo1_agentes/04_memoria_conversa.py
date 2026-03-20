# ============================================================
# MÓDULO 1 — AULA 1 | Arquivo 04: Memória de Conversa
# ============================================================
# CONCEITO FUNDAMENTAL:
# LLMs são "stateless" — não lembram nada entre chamadas.
# Para simular memória, você envia o HISTÓRICO COMPLETO
# a cada nova mensagem. É exatamente como chatbots funcionam!

from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1")

MODEL = os.getenv("MODEL")

# ── Histórico começa só com o system prompt ──────────────────
historico = [
    {"role": "system", "content": "Você é um tutor de Python e IA. Responda em português."}
]

def conversar(mensagem_usuario: str) -> str:
    """
    Conversa com memória — mantém o histórico entre mensagens.
    Cada chamada adiciona ao histórico e envia TUDO para o modelo.
    """
    # 1. Adiciona a mensagem do usuário ao histórico
    historico.append({"role": "user", "content": mensagem_usuario})

    # 2. Envia o histórico COMPLETO (o modelo "relembra" tudo)
    resposta = client.chat.completions.create(
        model=MODEL,
        messages=historico
    )

    resposta_texto = resposta.choices[0].message.content

    # 3. Adiciona a resposta do modelo ao histórico também
    historico.append({"role": "assistant", "content": resposta_texto})

    return resposta_texto


# ── Demonstração: o modelo lembra do contexto ────────────────
print("👤 Você: Meu nome é João e estou aprendendo IA com Python")
print("🤖 IA:", conversar("Meu nome é João e estou aprendendo IA com Python"))

print("\n" + "-"*50 + "\n")

print("👤 Você: Qual linguagem eu disse que estou aprendendo?")
print("🤖 IA:", conversar("Qual linguagem eu disse que estou aprendendo?"))

print("\n" + "-"*50 + "\n")

print("👤 Você: E qual foi meu nome?")
print("🤖 IA:", conversar("E qual foi meu nome?"))

# O modelo lembrou! Porque enviamos o histórico completo.

print("\n" + "="*60)
print(f"📋 Histórico atual: {len(historico)} mensagens")
print("   (system + 3 pares de user/assistant)")
