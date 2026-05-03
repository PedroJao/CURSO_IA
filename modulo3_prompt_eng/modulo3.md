# ✍️ Módulo 3 — Prompt Engineering

Neste módulo você aprende a se comunicar com LLMs de forma eficaz. Um prompt bem construído pode transformar uma resposta medíocre numa excepcional — sem mudar uma linha de código. O projeto final integra todas as técnicas num pipeline completo de suporte técnico.

> ⚠️ **Antes de começar:** certifique-se de ter seguido todos os passos do [README principal](../README.md) — WSL, UV, ambiente virtual ativo e arquivo `.env` configurado com `OPENROUTER_API_KEY` e `MODEL`.

---

## 🎯 O que você vai aprender

- Anatomia de um prompt completo: papel, contexto, instrução, formato e restrições
- Zero-shot prompting: quando usar e suas limitações
- Few-shot prompting: ensinar o modelo com exemplos
- Chain-of-Thought: forçar raciocínio passo a passo
- Structured Output: forçar JSON para integração com código
- Padrão ReAct: raciocínio + ação encadeados (base dos agentes)
- Meta-prompting: usar o LLM para melhorar seus próprios prompts
- Templates Jinja2: prompts reutilizáveis e dinâmicos

---

## 📦 Dependências

```bash
uv add openai python-dotenv jinja2
```

---

## 📂 Arquivos e ordem de execução

| Arquivo                        | Conceito                                        | Semana |
|--------------------------------|-------------------------------------------------|--------|
| `01_anatomia_prompt.py`        | Estrutura de um prompt e zero-shot              | 10     |
| `02_few_shot_cot.py`           | Few-shot prompting e Chain-of-Thought           | 11     |
| `03_tecnicas_avancadas.py`     | Structured Output, ReAct e Meta-prompting       | 12     |
| `04_templates_jinja2.py`       | Templates reutilizáveis com lógica condicional  | 13     |
| `05_projeto_sistema_prompts.py`| 🏁 Projeto final: pipeline completo de suporte  | 13     |

---

## ▶️ Como rodar

Execute a partir da raiz do projeto (`CURSO_IA/`):

```bash
uv run modulo3_prompt_eng/01_anatomia_prompt.py
uv run modulo3_prompt_eng/02_few_shot_cot.py
uv run modulo3_prompt_eng/03_tecnicas_avancadas.py
uv run modulo3_prompt_eng/04_templates_jinja2.py
uv run modulo3_prompt_eng/05_projeto_sistema_prompts.py
```

> 💡 Este módulo faz chamadas reais à API a cada arquivo. Se aparecer erro 429, aguarde alguns minutos e rode novamente.

---

## 🧠 Conceitos-chave

**Os 5 elementos de um prompt completo**

| Elemento    | Para que serve                              | Exemplo                              |
|-------------|---------------------------------------------|--------------------------------------|
| Papel       | Define quem o modelo deve ser               | "Você é um professor universitário"  |
| Contexto    | Informações de fundo necessárias            | "Estou explicando para iniciantes"   |
| Instrução   | O que exatamente fazer                      | "Explique o que é Machine Learning"  |
| Formato     | Como estruturar a resposta                  | "Use: DEFINIÇÃO / ANALOGIA / EXEMPLOS"|
| Restrições  | O que evitar ou limitar                     | "Evite termos técnicos sem explicar" |

**Zero-shot vs Few-shot**

| Técnica   | Exemplos fornecidos | Melhor para                          |
|-----------|---------------------|--------------------------------------|
| Zero-shot | Nenhum              | Tarefas simples e diretas            |
| Few-shot  | 2 a 5 exemplos      | Formato específico, estilo controlado|

**Chain-of-Thought**

Adicionar "Pense passo a passo" ou "Explique seu raciocínio antes de responder" melhora drasticamente resultados em problemas de lógica, matemática e análise — o modelo é forçado a não pular etapas.

**Padrão ReAct**

```
Thought: o que estou analisando...
Action: CALCULAR / BUSCAR / ANALISAR
Observation: resultado da ação...
(repete até ter a resposta)
Final Answer: resposta final
```

**Templates Jinja2**

```python
from jinja2 import Template

template = Template("Analise {{ tipo }} para público {{ publico }}.")
prompt = template.render(tipo="e-mail", publico="clientes VIP")
```

---

## ✅ Checklist de conclusão

- [ ] Conseguir explicar a diferença entre zero-shot e few-shot
- [ ] Escrever um prompt com os 5 elementos completos
- [ ] Forçar o modelo a responder em JSON e parsear com `json.loads()`
- [ ] Observar a diferença entre resposta com e sem Chain-of-Thought
- [ ] Criar um template Jinja2 com pelo menos uma variável
- [ ] Rodar o projeto final e ver o pipeline de 3 etapas funcionando

---

## ➡️ Próximo módulo

[Módulo 4 — Ferramentas e Memória](../modulo4_ferramentas/modulo4.md)