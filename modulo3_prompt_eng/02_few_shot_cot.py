# ============================================================
# MÓDULO 3 — PROMPT ENGINEERING | Arquivo 02: Few-shot e CoT
# Semana 11 — Few-shot Prompting e Chain-of-Thought
# ============================================================
#
# CONCEITO:
# Few-shot = fornecer exemplos no prompt para ensinar o modelo
# o padrão exato que você quer.
#
# Chain-of-Thought = pedir ao modelo para "pensar em voz alta"
# antes de responder. Melhora drasticamente o raciocínio.

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


# ── PARTE 1: Few-shot Prompting ───────────────────────────────
print("=" * 60)
print("  🎯 PARTE 1: Few-shot Prompting")
print("=" * 60)
print("""
Few-shot = você fornece exemplos de entrada/saída no próprio prompt.
O modelo aprende o PADRÃO dos exemplos e aplica ao novo caso.

Quando usar:
  ✅ Quando o formato de saída importa muito
  ✅ Quando zero-shot gera respostas inconsistentes
  ✅ Quando você quer um estilo específico de resposta
""")

# Exemplo: classificação de sentimento com formato controlado
print("📌 Comparação: Zero-shot vs Few-shot para classificação\n")

texto_teste = "O atendimento foi ok mas o prazo de entrega foi péssimo."

# Zero-shot — sem exemplos
prompt_zero = f"Classifique o sentimento: '{texto_teste}'"
resp_zero = chamar_modelo(prompt_zero)
print(f"🔵 Zero-shot:\n   {resp_zero}\n")

# Few-shot — com exemplos que ensinam o formato exato
prompt_few = f"""Classifique o sentimento dos textos. Responda APENAS no formato: SENTIMENTO | ASPECTO PRINCIPAL

Exemplos:
Texto: "Adorei o produto, superou minhas expectativas!"
Resposta: POSITIVO | qualidade do produto

Texto: "Entrega no prazo, nada demais."
Resposta: NEUTRO | pontualidade

Texto: "Péssimo atendimento, nunca mais compro aqui."
Resposta: NEGATIVO | atendimento ao cliente

Texto: "O produto é ótimo mas o frete foi caro demais."
Resposta: MISTO | custo-benefício

Agora classifique:
Texto: "{texto_teste}"
Resposta:"""

resp_few = chamar_modelo(prompt_few)
print(f"🟢 Few-shot:\n   {resp_few}")
print("""
Observe: o few-shot forçou o modelo a seguir o formato
"SENTIMENTO | ASPECTO" — muito mais útil para processar
programaticamente do que uma resposta em texto livre.
""")


# ── PARTE 2: Few-shot para extração estruturada ──────────────
print("=" * 60)
print("  📋 PARTE 2: Few-shot para Extração de Dados")
print("=" * 60)
print("""
Um dos usos mais poderosos do few-shot é extrair informações
estruturadas de texto não estruturado.
""")

prompt_extracao = """Extraia as informações de vagas de emprego no formato indicado.

Exemplo 1:
Texto: "Buscamos Dev Python Pleno, remoto, salário 6k-8k, experiência com FastAPI obrigatória."
Cargo: Desenvolvedor Python
Nível: Pleno
Modalidade: Remoto
Salário: R$6.000 - R$8.000
Tecnologias: FastAPI

Exemplo 2:
Texto: "Vaga presencial SP para Analista de Dados Jr, até R$4.500, desejável Power BI e SQL."
Cargo: Analista de Dados
Nível: Júnior
Modalidade: Presencial (São Paulo)
Salário: até R$4.500
Tecnologias: Power BI, SQL

Agora extraia:
Texto: "Procuramos Engenheiro de ML Sênior para trabalho híbrido em BH. Remuneração: R$15k-20k. Requisitos: PyTorch, MLflow e experiência com deploy de modelos em produção."
"""

resp_extracao = chamar_modelo(prompt_extracao)
print("📌 Extração de vaga de emprego:")
print(resp_extracao)


# ── PARTE 3: Chain-of-Thought (CoT) ──────────────────────────
print("\n" + "=" * 60)
print("  🧠 PARTE 3: Chain-of-Thought (CoT)")
print("=" * 60)
print("""
Chain-of-Thought = pedir ao modelo para mostrar o raciocínio
passo a passo antes de dar a resposta final.

Por que funciona?
  • Força o modelo a não "pular etapas"
  • Erros no raciocínio ficam visíveis e corrigíveis
  • Melhora muito em problemas de lógica, matemática e análise

Como ativar: basta adicionar "Pense passo a passo" ou
"Explique seu raciocínio antes de responder".
""")

problema = """Uma empresa de e-commerce tem os seguintes dados do mês:
- Visitantes únicos: 50.000
- Adicionaram ao carrinho: 8.000
- Finalizaram a compra: 1.200
- Ticket médio: R$ 180,00
- Custo de aquisição por visitante: R$ 2,50

Perguntas:
1. Qual é a taxa de conversão do carrinho para compra?
2. Qual foi o faturamento total?
3. Qual foi o ROI da campanha de aquisição?
4. Qual etapa do funil está mais crítica e por quê?"""

# Sem CoT
print("🔵 Sem Chain-of-Thought:")
resp_sem_cot = chamar_modelo(problema, "Você é um analista de e-commerce. Responda em português.")
print(resp_sem_cot[:400] + "..." if len(resp_sem_cot) > 400 else resp_sem_cot)

print("\n" + "-" * 60 + "\n")

# Com CoT
print("🟢 Com Chain-of-Thought:")
problema_cot = "Pense passo a passo, mostrando cada cálculo antes de responder.\n\n" + problema
resp_com_cot = chamar_modelo(problema_cot, "Você é um analista de e-commerce. Responda em português.")
print(resp_com_cot)


# ── PARTE 4: CoT com Few-shot (o combo mais poderoso) ────────
print("\n" + "=" * 60)
print("  💥 PARTE 4: Few-shot + CoT combinados")
print("=" * 60)
print("""
Combinar few-shot + CoT é a técnica mais poderosa para
problemas complexos: você mostra exemplos de raciocínio
passo a passo, e o modelo segue o mesmo padrão.
""")

prompt_combo = """Analise bugs de código mostrando o raciocínio passo a passo.

Exemplo:
Código: 
def calcular_media(numeros):
    return sum(numeros) / len(numeros)

resultado = calcular_media([])

Raciocínio:
1. A função recebe uma lista vazia []
2. sum([]) retorna 0 — ok
3. len([]) retorna 0 — problema!
4. 0 / 0 causa ZeroDivisionError

Bug: divisão por zero quando a lista está vazia.
Correção: verificar se a lista está vazia antes de dividir.

Agora analise:
Código:
numeros = [1, 2, 3, 4, 5]
print(numeros[10])
"""

resp_combo = chamar_modelo(prompt_combo, "Você é um revisor de código sênior. Responda em português.")
print(resp_combo)


# ── RESUMO ───────────────────────────────────────────────────
print("\n" + "=" * 60)
print("✅ RESUMO DO ARQUIVO 02")
print("=" * 60)
print("""
O que você aprendeu:
  • Few-shot: ensinar o modelo com exemplos de entrada/saída
  • Como controlar o formato da resposta com exemplos
  • Few-shot para extração de dados estruturados
  • Chain-of-Thought: forçar raciocínio passo a passo
  • O combo few-shot + CoT para problemas complexos

Próximo arquivo: 03_tecnicas_avancadas.py
  → Structured Output, ReAct e Meta-prompting
""")