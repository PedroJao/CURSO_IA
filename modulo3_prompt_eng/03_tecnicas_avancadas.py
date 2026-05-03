# ============================================================
# MÓDULO 3 — PROMPT ENGINEERING | Arquivo 03: Técnicas Avançadas
# Semana 12 — Structured Output, ReAct e Meta-prompting
# ============================================================
#
# CONCEITO:
# Técnicas avançadas para cenários profissionais:
#   • Structured Output → forçar JSON para integração com código
#   • ReAct             → raciocínio + ação encadeados (base dos agentes)
#   • Meta-prompting    → usar o LLM para melhorar seus próprios prompts

from dotenv import load_dotenv
from openai import OpenAI
import os
import json

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


# ── PARTE 1: Structured Output (JSON forçado) ────────────────
print("=" * 60)
print("  📦 PARTE 1: Structured Output")
print("=" * 60)
print("""
Structured Output = forçar o modelo a responder em JSON válido.

ESSENCIAL para integrar LLMs em sistemas reais:
  • O JSON pode ser parseado e salvo no banco de dados
  • Pode alimentar outras APIs ou serviços
  • Elimina a necessidade de processar texto não estruturado

Regras para obter JSON confiável:
  1. Instrua explicitamente no system: "responda APENAS com JSON"
  2. Defina o schema exato que você quer
  3. Diga "sem markdown, sem explicações"
  4. Trate erros de parsing com try/except
""")

system_json = """Você extrai informações de textos e retorna APENAS JSON válido.
Sem markdown, sem explicações, sem texto fora do JSON."""

# Exemplo 1: extrair dados de um artigo de notícia
texto_noticia = """
São Paulo, 15 de março — A startup brasileira TechIA anunciou hoje uma rodada
série B de R$ 50 milhões liderada pelo fundo Vinci Partners. A empresa, fundada
em 2021 por Marina Costa e Rafael Souza, desenvolve soluções de IA para o setor
de saúde e já atende 200 hospitais em 12 estados. Com o aporte, planeja expandir
para América Latina até o final de 2025 e contratar 150 funcionários.
"""

prompt_json = f"""Extraia as informações do texto e retorne neste formato JSON exato:
{{
  "empresa": "string",
  "valor_rodada": "string",
  "fundo_lider": "string",
  "ano_fundacao": number,
  "fundadores": ["string"],
  "setor": "string",
  "clientes": number,
  "estados": number,
  "planos": ["string"]
}}

Texto:
{texto_noticia}"""

print("📌 Extração de notícia para JSON:")
resposta_raw = chamar_modelo(prompt_json, system_json)
print(f"Raw: {resposta_raw}\n")

# Parsear o JSON com segurança
try:
    limpo = resposta_raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    dados = json.loads(limpo)
    print("✅ JSON parseado com sucesso!")
    print(f"  Empresa:    {dados.get('empresa')}")
    print(f"  Rodada:     {dados.get('valor_rodada')}")
    print(f"  Fundadores: {', '.join(dados.get('fundadores', []))}")
    print(f"  Clientes:   {dados.get('clientes')} hospitais")
except json.JSONDecodeError as e:
    print(f"❌ Erro ao parsear JSON: {e}")
    print("Dica: ajuste o system prompt para ser mais restritivo")


# ── PARTE 2: ReAct (Reason + Act) ────────────────────────────
print("\n" + "=" * 60)
print("  🤖 PARTE 2: ReAct — Reason + Act")
print("=" * 60)
print("""
ReAct é o padrão que está por trás dos agentes de IA modernos.
O modelo alterna entre:
  Thought    → o que estou pensando agora?
  Action     → o que vou fazer? (buscar, calcular, responder)
  Observation → o que observei do resultado?

Repetindo até chegar na resposta final.

Aqui vamos simular o padrão ReAct manualmente para entender
o que frameworks como LangChain fazem automaticamente.
""")

system_react = """Você resolve problemas usando raciocínio estruturado.

Para cada problema, siga EXATAMENTE este formato:
Thought: [o que você está analisando ou pensando]
Action: [CALCULAR | BUSCAR | ANALISAR | RESPONDER] - [descrição da ação]
Observation: [resultado da ação]
... (repita Thought/Action/Observation quantas vezes precisar)
Final Answer: [sua resposta final clara e direta]"""

problema_react = """Um desenvolvedor precisa escolher entre duas opções para seu projeto:

Opção A: Servidor próprio
- Custo inicial: R$ 8.000
- Custo mensal: R$ 800
- Capacidade: 10.000 usuários/mês

Opção B: Cloud (AWS)
- Custo inicial: R$ 0
- Custo mensal: R$ 200 + R$ 0,05 por usuário acima de 1.000
- Capacidade: ilimitada

O projeto espera começar com 500 usuários e crescer 20% ao mês.
Em qual mês a Opção B se torna mais cara que a Opção A?
Qual é a melhor escolha considerando 24 meses?"""

print("📌 Problema de análise de custo com ReAct:")
resp_react = chamar_modelo(problema_react, system_react)
print(resp_react)


# ── PARTE 3: Meta-prompting ───────────────────────────────────
print("\n" + "=" * 60)
print("  🔧 PARTE 3: Meta-prompting")
print("=" * 60)
print("""
Meta-prompting = usar o LLM para melhorar seus próprios prompts.

Em vez de ficar tentando e errando manualmente, você pede
ao modelo que analise e reescreva um prompt ruim.
Economiza horas de trial-and-error.
""")

system_meta = """Você é um especialista em Prompt Engineering com anos de experiência.
Analise prompts e os melhore aplicando as melhores práticas.

Responda sempre neste formato:
PROBLEMAS: [lista dos problemas encontrados]
PROMPT MELHORADO:
---
[o prompt reescrito]
---
EXPLICAÇÃO: [por que as mudanças melhoram o resultado]"""

prompts_ruins = [
    "me ajuda com python",
    "faz um email pro cliente reclamando do prazo",
    "resume esse texto de forma boa",
]

for prompt in prompts_ruins:
    print(f"\n📌 Melhorando: '{prompt}'")
    print("-" * 50)
    resultado = chamar_modelo(
        f"Melhore este prompt:\n\n'{prompt}'",
        system_meta
    )
    print(resultado)
    print()


# ── RESUMO ───────────────────────────────────────────────────
print("=" * 60)
print("✅ RESUMO DO ARQUIVO 03")
print("=" * 60)
print("""
O que você aprendeu:
  • Structured Output: forçar JSON para integração com código
  • Como parsear a resposta com segurança usando try/except
  • ReAct: o padrão Thought/Action/Observation dos agentes
  • Meta-prompting: usar o LLM para melhorar seus prompts

Próximo arquivo: 04_templates_jinja2.py
  → Templates de prompts reutilizáveis e dinâmicos
""")