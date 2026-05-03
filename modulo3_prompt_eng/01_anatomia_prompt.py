# ============================================================
# MÓDULO 3 — PROMPT ENGINEERING | Arquivo 01: Anatomia de um Prompt
# Semana 10 — System, User, Contexto, Instrução e Formato
# ============================================================
# Antes de rodar: uv add openai python-dotenv
#
# CONCEITO:
# Prompt Engineering é a arte de se comunicar com LLMs de forma
# eficaz. Um prompt bem construído pode transformar uma resposta
# medíocre numa resposta excepcional — sem mudar uma linha de
# código ou gastar mais em API.
#
# Neste arquivo você aprende a anatomia de um prompt completo
# e a técnica mais básica: Zero-shot prompting.

from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1")

MODEL = os.getenv("MODEL")


def chamar_modelo(user_msg: str, system_msg: str = "Você é um assistente útil. Responda em português.") -> str:
    resposta = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user",   "content": user_msg}
        ]
    )
    return resposta.choices[0].message.content


# ── PARTE 1: Anatomia de um Prompt Completo ──────────────────
print("=" * 60)
print("  🔬 PARTE 1: Anatomia de um Prompt")
print("=" * 60)
print("""
Um prompt bem estruturado tem até 5 elementos:

  1. PAPEL (Role)      → quem o modelo deve ser
  2. CONTEXTO          → informações de fundo necessárias
  3. INSTRUÇÃO         → o que exatamente fazer
  4. FORMATO           → como a resposta deve ser estruturada
  5. RESTRIÇÕES        → o que evitar ou limitar

Nem todo prompt precisa dos 5 — mas quanto mais completo,
mais previsível e controlado será o resultado.
""")

# Prompt FRACO — sem estrutura
prompt_fraco = "Me fala sobre machine learning"
print("🔴 Prompt FRACO:")
print(f"   '{prompt_fraco}'")
print("\nResposta:")
print(chamar_modelo(prompt_fraco))

print("\n" + "-" * 60 + "\n")

# Prompt FORTE — com todos os elementos
system_forte = """Você é um professor universitário de Ciência de Dados.
Seu estilo é didático e usa analogias do cotidiano para explicar conceitos técnicos."""

prompt_forte = """Contexto: estou explicando Machine Learning para alunos do primeiro semestre, sem conhecimento prévio de programação.

Instrução: explique o que é Machine Learning.

Formato: use exatamente esta estrutura:
  DEFINIÇÃO: (1 frase simples)
  ANALOGIA: (1 analogia do dia a dia)
  EXEMPLOS: (3 exemplos práticos em bullet points)

Restrição: evite termos técnicos como algoritmo, modelo ou dataset sem explicar antes."""

print("🟢 Prompt FORTE:")
print(f"   System: '{system_forte[:60]}...'")
print(f"   User: estruturado com contexto, instrução, formato e restrições")
print("\nResposta:")
print(chamar_modelo(prompt_forte, system_forte))


# ── PARTE 2: O Poder do System Prompt ────────────────────────
print("\n" + "=" * 60)
print("  ⚙️  PARTE 2: O Poder do System Prompt")
print("=" * 60)
print("""
O system prompt é o "DNA" do seu agente.
A mesma pergunta do usuário gera respostas completamente
diferentes dependendo do system prompt configurado.
""")

pergunta = "O que devo fazer quando meu código não funciona?"

personas = {
    "👨‍🏫 Professor paciente": """Você é um professor de programação muito paciente.
    Sempre elogia o esforço do aluno antes de corrigir.
    Usa linguagem simples e passos pequenos.""",

    "👨‍💼 Tech Lead sênior": """Você é um tech lead sênior com 15 anos de experiência.
    Seja direto, técnico e eficiente. Sem rodeios.""",

    "🤣 Programador bem-humorado": """Você é um programador que ama humor.
    Responda de forma útil mas sempre inclua uma piada ou meme de programação relevante.""",
}

for persona, system in personas.items():
    print(f"\n{persona}:")
    print("-" * 40)
    resposta = chamar_modelo(pergunta, system)
    print(resposta[:300] + "..." if len(resposta) > 300 else resposta)


# ── PARTE 3: Zero-shot Prompting ─────────────────────────────
print("\n" + "=" * 60)
print("  🎯 PARTE 3: Zero-shot Prompting")
print("=" * 60)
print("""
Zero-shot = nenhum exemplo fornecido.
Você só dá a instrução e confia que o modelo entende.

Funciona bem para tarefas simples e diretas.
Falha em tarefas que exigem formato específico ou raciocínio complexo.
""")

tarefas_zero_shot = [
    ("Classificação simples",
     "Classifique o sentimento do texto como POSITIVO, NEGATIVO ou NEUTRO.\n\nTexto: 'O produto chegou rápido mas a qualidade deixou a desejar.'"),

    ("Tradução",
     "Traduza para inglês: 'Inteligência Artificial está transformando o mundo.'"),

    ("Resumo",
     "Resuma em uma frase: 'Machine Learning é um subcampo da Inteligência Artificial que permite que sistemas aprendam e melhorem automaticamente através da experiência, sem serem explicitamente programados para cada tarefa.'"),
]

for nome, prompt in tarefas_zero_shot:
    print(f"\n📌 {nome}:")
    print(f"   Prompt: '{prompt[:80]}...'")
    print(f"   Resposta: {chamar_modelo(prompt)}")


# ── RESUMO ───────────────────────────────────────────────────
print("\n" + "=" * 60)
print("✅ RESUMO DO ARQUIVO 01")
print("=" * 60)
print("""
O que você aprendeu:
  • Os 5 elementos de um prompt completo (papel, contexto,
    instrução, formato, restrições)
  • Como o system prompt define o "personagem" do modelo
  • Zero-shot prompting: quando usar e suas limitações

Próximo arquivo: 02_few_shot_cot.py
  → Few-shot prompting e Chain-of-Thought
""")