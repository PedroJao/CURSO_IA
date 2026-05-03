# ============================================================
# MÓDULO 3 — PROMPT ENGINEERING | Arquivo 04: Templates com Jinja2
# Semana 13 — Prompts Reutilizáveis e Dinâmicos
# ============================================================
# Antes de rodar: uv add jinja2
#
# CONCEITO:
# Em projetos reais você vai reutilizar os mesmos prompts com
# variáveis diferentes — produto, cliente, idioma, contexto...
# Hardcodar tudo dentro do código é difícil de manter.
#
# Jinja2 é o sistema de templates mais usado em Python.
# Com ele você separa o "esqueleto" do prompt das variáveis,
# igual ao que frameworks web fazem com HTML.

from dotenv import load_dotenv
from openai import OpenAI
from jinja2 import Template, Environment, FileSystemLoader
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


# ── PARTE 1: Template Básico com Jinja2 ──────────────────────
print("=" * 60)
print("  📝 PARTE 1: Template Básico com Jinja2")
print("=" * 60)
print("""
Jinja2 usa {{ variavel }} para interpolar valores
e {% if %}, {% for %} para lógica dentro do template.
""")

# Template simples — análise de produto
template_analise = Template("""
Você é um especialista em {{ area }}.

Analise o seguinte {{ tipo }} e forneça:
1. Pontos fortes (máximo {{ max_pontos }} itens)
2. Pontos de melhoria (máximo {{ max_pontos }} itens)
3. Nota geral de 0 a 10

{{ tipo }} para análise:
{{ conteudo }}

Responda de forma {{ estilo }}.
""")

# Usando o mesmo template para contextos diferentes
casos = [
    {
        "area": "UX Writing",
        "tipo": "mensagem de erro",
        "max_pontos": 3,
        "estilo": "objetiva e construtiva",
        "conteudo": "Erro 404: Página não encontrada. Tente novamente mais tarde."
    },
    {
        "area": "comunicação corporativa",
        "tipo": "e-mail profissional",
        "max_pontos": 2,
        "estilo": "direta e prática",
        "conteudo": "Oi, precisamos conversar sobre o projeto. Me chama quando puder. Abs"
    }
]

for caso in casos:
    prompt = template_analise.render(**caso)
    print(f"\n📌 Analisando {caso['tipo']}:")
    print("-" * 50)
    print(chamar_modelo(prompt))


# ── PARTE 2: Templates com Lógica Condicional ────────────────
print("\n" + "=" * 60)
print("  🔀 PARTE 2: Templates com Lógica Condicional")
print("=" * 60)
print("""
Com {% if %} e {% for %} você cria prompts que se adaptam
automaticamente ao contexto — sem precisar de múltiplos prompts.
""")

template_report = Template("""
Crie um relatório de análise de código para o seguinte trecho em {{ linguagem }}.

{% if nivel_dev == "junior" %}
Use linguagem simples, explique cada problema como se fosse para alguém aprendendo.
{% elif nivel_dev == "senior" %}
Seja técnico e direto. Mencione padrões de design e boas práticas avançadas.
{% endif %}

{% if incluir_correcao %}
Para cada problema encontrado, forneça também o código corrigido.
{% endif %}

Foque nos seguintes aspectos:
{% for aspecto in aspectos %}
- {{ aspecto }}
{% endfor %}

Código:
{{ codigo }}
""")

codigo_exemplo = """
def buscar_usuarios(db, status):
    result = []
    for i in range(1000):
        u = db.query("SELECT * FROM users WHERE status='" + status + "'")
        result.append(u)
    return result
"""

configs = [
    {
        "linguagem": "Python",
        "nivel_dev": "junior",
        "incluir_correcao": True,
        "aspectos": ["segurança", "performance"],
        "codigo": codigo_exemplo
    },
    {
        "linguagem": "Python",
        "nivel_dev": "senior",
        "incluir_correcao": False,
        "aspectos": ["SQL injection", "N+1 query problem", "type hints"],
        "codigo": codigo_exemplo
    }
]

for config in configs:
    prompt = template_report.render(**config)
    print(f"\n📌 Revisão para dev {config['nivel_dev']}:")
    print("-" * 50)
    print(chamar_modelo(prompt, "Você é um revisor de código experiente. Responda em português."))


# ── PARTE 3: Biblioteca de Prompts Reutilizáveis ─────────────
print("\n" + "=" * 60)
print("  📚 PARTE 3: Biblioteca de Prompts")
print("=" * 60)
print("""
Em projetos profissionais, prompts ficam centralizados em um
dicionário ou arquivo — fácil de versionar, testar e manter.
""")

# Biblioteca de prompts da empresa (simulado)
PROMPT_LIBRARY = {
    "classificar_ticket": Template("""
Classifique o ticket de suporte abaixo.

Categorias disponíveis: {{ categorias | join(', ') }}
Prioridades: BAIXA, MÉDIA, ALTA, CRÍTICA

Retorne APENAS JSON no formato:
{"categoria": "string", "prioridade": "string", "resumo": "string (max 20 palavras)"}

Ticket: {{ ticket }}
"""),

    "responder_cliente": Template("""
Você é um agente de suporte da {{ empresa }}.
Tom de voz: {{ tom }}.

Responda ao cliente abaixo de forma {{ tamanho }}.
{% if incluir_link %}
Inclua o link {{ link_ajuda }} quando relevante.
{% endif %}

Mensagem do cliente:
{{ mensagem }}
"""),

    "gerar_titulo": Template("""
Gere {{ quantidade }} opções de título para o seguinte conteúdo.
Estilo: {{ estilo }}
Público-alvo: {{ publico }}

Conteúdo: {{ conteudo }}

Retorne apenas os títulos, um por linha, sem numeração.
"""),
}


def usar_prompt(nome: str, **kwargs) -> str:
    if nome not in PROMPT_LIBRARY:
        raise ValueError(f"Prompt '{nome}' não encontrado na biblioteca.")
    prompt = PROMPT_LIBRARY[nome].render(**kwargs)
    return chamar_modelo(prompt)


# Testando a biblioteca
print("\n📌 Classificando ticket de suporte:")
resultado = usar_prompt(
    "classificar_ticket",
    categorias=["Faturamento", "Suporte Técnico", "Cancelamento", "Dúvida Geral"],
    ticket="Fui cobrado duas vezes no cartão esse mês e não consigo acessar minha conta para verificar!"
)
print(resultado)

print("\n📌 Gerando títulos para blog post:")
resultado = usar_prompt(
    "gerar_titulo",
    quantidade=4,
    estilo="chamativo e direto, sem clickbait",
    publico="desenvolvedores Python iniciantes",
    conteudo="Como usar variáveis de ambiente para proteger credenciais em projetos Python"
)
print(resultado)


# ── RESUMO ───────────────────────────────────────────────────
print("\n" + "=" * 60)
print("✅ RESUMO DO ARQUIVO 04")
print("=" * 60)
print("""
O que você aprendeu:
  • Templates Jinja2 com {{ variavel }} para interpolação
  • Lógica condicional {% if %} e loops {% for %} em prompts
  • Como adaptar o mesmo prompt para contextos diferentes
  • Biblioteca centralizada de prompts reutilizáveis

Próximo arquivo: 05_projeto_sistema_prompts.py
  → Projeto final: sistema completo de prompts para um assistente
""")