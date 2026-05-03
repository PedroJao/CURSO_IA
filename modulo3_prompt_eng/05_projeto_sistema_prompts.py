# ============================================================
# MÓDULO 3 — PROMPT ENGINEERING | Arquivo 05: Projeto Final
# Semana 13 — Sistema Completo de Prompts para um Assistente
# ============================================================
#
# PROJETO: Assistente de Suporte Técnico com sistema de prompts
# profissional que integra todas as técnicas do módulo.
#
# O sistema vai:
#   1. Classificar a mensagem do usuário (JSON estruturado)
#   2. Escolher o prompt ideal para cada tipo de problema
#   3. Gerar uma resposta com Chain-of-Thought interno
#   4. Avaliar a própria resposta (meta-prompting)
#   5. Entregar a resposta final formatada

from dotenv import load_dotenv
from openai import OpenAI
from jinja2 import Template
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1")

MODEL = os.getenv("MODEL")

print("=" * 60)
print("  🤖 PROJETO FINAL — Assistente de Suporte Técnico")
print("=" * 60)


# ── FUNÇÕES BASE ──────────────────────────────────────────────
def chamar_modelo(user_msg: str, system_msg: str) -> str:
    resposta = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user",   "content": user_msg}
        ]
    )
    return resposta.choices[0].message.content


def parsear_json(texto: str) -> dict:
    """Parseia JSON com tratamento de erros robusto."""
    try:
        limpo = texto.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(limpo)
    except json.JSONDecodeError:
        return {}


# ── ETAPA 1: CLASSIFICADOR DE INTENÇÃO ───────────────────────
SYSTEM_CLASSIFICADOR = """Você classifica mensagens de suporte técnico.
Retorne APENAS JSON válido, sem markdown, sem explicações."""

TEMPLATE_CLASSIFICAR = Template("""Classifique esta mensagem de suporte:

Categorias: bug, duvida_uso, erro_instalacao, solicitacao_feature, outro
Urgências: baixa, media, alta, critica
Sentimento: frustrado, neutro, satisfeito

Retorne exatamente:
{
  "categoria": "string",
  "urgencia": "string",
  "sentimento": "string",
  "resumo": "string (max 15 palavras)"
}

Mensagem: {{ mensagem }}""")


def classificar_mensagem(mensagem: str) -> dict:
    prompt = TEMPLATE_CLASSIFICAR.render(mensagem=mensagem)
    resposta = chamar_modelo(prompt, SYSTEM_CLASSIFICADOR)
    classificacao = parsear_json(resposta)
    if not classificacao:
        classificacao = {"categoria": "outro", "urgencia": "media",
                         "sentimento": "neutro", "resumo": mensagem[:50]}
    return classificacao


# ── ETAPA 2: TEMPLATES DE RESPOSTA POR CATEGORIA ─────────────
TEMPLATES_RESPOSTA = {
    "bug": Template("""Você é um engenheiro de suporte técnico sênior.
O usuário está com sentimento {{ sentimento }} — ajuste seu tom para ser {{ tom_sugerido }}.

Problema reportado: {{ resumo }}
Urgência: {{ urgencia }}

Responda seguindo este raciocínio interno (não mostre ao usuário):
1. Confirme que entendeu o problema
2. Identifique a causa mais provável
3. Elabore os passos de solução

Formato da resposta ao usuário:
- Reconhecimento empático (1 frase)
- Causa provável
- Passos para resolver (numerados)
- Próximo passo caso não resolva"""),

    "duvida_uso": Template("""Você é um especialista no produto, didático e paciente.
O usuário está com sentimento {{ sentimento }}.

Dúvida: {{ resumo }}

Explique de forma clara e direta:
- Resposta direta à dúvida
- Exemplo prático (se aplicável)
- Dica adicional relacionada"""),

    "erro_instalacao": Template("""Você é um especialista em instalação e configuração.
O usuário está com sentimento {{ sentimento }} — seja especialmente paciente.

Problema: {{ resumo }}
Urgência: {{ urgencia }}

Guie o usuário passo a passo:
- Confirmação do ambiente (OS, versão)
- Passos de diagnóstico
- Solução mais comum
- Alternativa caso não funcione"""),

    "outro": Template("""Você é um assistente de suporte prestativo.
Mensagem: {{ resumo }}
Sentimento do usuário: {{ sentimento }}

Responda de forma útil e direcione para o canal correto se necessário."""),
}

TONS_POR_SENTIMENTO = {
    "frustrado": "empático e calmo, reconhecendo a frustração",
    "neutro":    "profissional e objetivo",
    "satisfeito": "amigável e eficiente",
}


def gerar_resposta(mensagem: str, classificacao: dict) -> str:
    categoria = classificacao.get("categoria", "outro")
    template = TEMPLATES_RESPOSTA.get(categoria, TEMPLATES_RESPOSTA["outro"])

    system_prompt = template.render(
        sentimento=classificacao.get("sentimento", "neutro"),
        tom_sugerido=TONS_POR_SENTIMENTO.get(classificacao.get("sentimento", "neutro"), "profissional"),
        resumo=classificacao.get("resumo", mensagem),
        urgencia=classificacao.get("urgencia", "media"),
    )

    return chamar_modelo(mensagem, system_prompt)


# ── ETAPA 3: AVALIADOR DE QUALIDADE (META-PROMPTING) ─────────
SYSTEM_AVALIADOR = """Você avalia qualidade de respostas de suporte técnico.
Retorne APENAS JSON válido."""

TEMPLATE_AVALIAR = Template("""Avalie esta resposta de suporte em 3 critérios (nota 1-10):

Mensagem original: {{ mensagem }}
Classificação: {{ categoria }} | {{ urgencia }} | {{ sentimento }}

Resposta gerada:
{{ resposta }}

Retorne:
{
  "clareza": number,
  "empatia": number,
  "utilidade": number,
  "nota_geral": number,
  "aprovada": boolean,
  "sugestao": "string (se nota_geral < 7, sugira melhoria em 1 frase)"
}""")


def avaliar_resposta(mensagem: str, classificacao: dict, resposta: str) -> dict:
    prompt = TEMPLATE_AVALIAR.render(
        mensagem=mensagem,
        categoria=classificacao.get("categoria"),
        urgencia=classificacao.get("urgencia"),
        sentimento=classificacao.get("sentimento"),
        resposta=resposta
    )
    resultado = chamar_modelo(prompt, SYSTEM_AVALIADOR)
    return parsear_json(resultado)


# ── PIPELINE COMPLETO ─────────────────────────────────────────
def processar_ticket(mensagem: str) -> None:
    print(f"\n{'='*60}")
    print(f"📨 Mensagem: {mensagem}")
    print("=" * 60)

    # Etapa 1: Classificar
    print("\n🔍 Etapa 1: Classificando...")
    classificacao = classificar_mensagem(mensagem)
    print(f"   Categoria: {classificacao.get('categoria')}")
    print(f"   Urgência:  {classificacao.get('urgencia')}")
    print(f"   Sentimento:{classificacao.get('sentimento')}")

    # Etapa 2: Gerar resposta
    print("\n💬 Etapa 2: Gerando resposta...")
    resposta = gerar_resposta(mensagem, classificacao)
    print(f"\n{resposta}")

    # Etapa 3: Avaliar qualidade
    print("\n📊 Etapa 3: Avaliando qualidade...")
    avaliacao = avaliar_resposta(mensagem, classificacao, resposta)
    if avaliacao:
        nota = avaliacao.get('nota_geral', '?')
        aprovada = "✅" if avaliacao.get('aprovada') else "⚠️"
        print(f"   {aprovada} Nota geral: {nota}/10")
        print(f"   Clareza: {avaliacao.get('clareza')}/10 | "
              f"Empatia: {avaliacao.get('empatia')}/10 | "
              f"Utilidade: {avaliacao.get('utilidade')}/10")
        if avaliacao.get("sugestao"):
            print(f"   💡 Sugestão: {avaliacao.get('sugestao')}")


# ── TESTANDO O SISTEMA ────────────────────────────────────────
tickets = [
    "Não consigo instalar a biblioteca, aparece erro de permissão toda vez que rodo pip install",
    "Como faço para exportar meus dados para CSV? Procurei na documentação mas não achei",
    "URGENTE: o sistema caiu em produção e estamos perdendo vendas!! Precisamos de ajuda AGORA",
]

for ticket in tickets:
    processar_ticket(ticket)

# ── RESUMO FINAL ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("✅ MÓDULO 3 — PROMPT ENGINEERING CONCLUÍDO!")
print("=" * 60)
print("""
Técnicas que você dominou:
  ✅ Anatomia de um prompt (papel, contexto, instrução, formato, restrições)
  ✅ Zero-shot prompting
  ✅ Few-shot prompting para controle de formato
  ✅ Chain-of-Thought para raciocínio complexo
  ✅ Structured Output com JSON e parsing seguro
  ✅ Padrão ReAct (Reason + Act)
  ✅ Meta-prompting para otimização de prompts
  ✅ Templates Jinja2 reutilizáveis com lógica condicional
  ✅ Pipeline completo integrando múltiplas técnicas

➡️  Próximo: Módulo 4 — Ferramentas e Memória
    O agente vai ganhar superpoderes: busca na web,
    leitura de PDFs e memória de longo prazo!
""")