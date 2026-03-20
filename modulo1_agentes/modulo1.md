# 📡 Módulo 1 — Fundação: LLMs e APIs

Neste módulo você faz sua primeira conexão real com um modelo de linguagem via Python, entende como a API funciona por dentro e constrói um chat interativo com memória de conversa.

> ⚠️ **Antes de começar:** certifique-se de ter seguido todos os passos do [README principal](../README.md) — WSL, UV, ambiente virtual ativo e arquivo `.env` configurado com `OPENROUTER_API_KEY` e `MODEL`.

---

## 🎯 O que você vai aprender

- Como LLMs funcionam: tokens, roles e estrutura de mensagens
- Fazer chamadas reais à API de um LLM com Python
- Diferença entre `system`, `user` e `assistant`
- Escrever funções reutilizáveis para chamadas ao modelo
- Por que LLMs são stateless e como simular memória com histórico
- Construir um chat interativo completo no terminal

---

## 📦 Dependências

```bash
uv add openai python-dotenv
```

---

## 📂 Arquivos e ordem de execução

| Arquivo                       | Conceito                                  |
|-------------------------------|-------------------------------------------|
| `01_setup.py`                 | Verifica se o ambiente está configurado   |
| `02_primeira_chamada.py`      | Primeira chamada real a um LLM            |
| `03_funcao_reutilizavel.py`   | Funções limpas com diferentes personas    |
| `04_memoria_conversa.py`      | Histórico de mensagens e memória          |
| `05_desafio_chat.py`          | 🏁 Projeto final: chat interativo         |

---

## ▶️ Como rodar

Execute a partir da raiz do projeto (`CURSO_IA/`):

```bash
uv run modulo1_agentes/01_setup.py
uv run modulo1_agentes/02_primeira_chamada.py
uv run modulo1_agentes/03_funcao_reutilizavel.py
uv run modulo1_agentes/04_memoria_conversa.py
uv run modulo1_agentes/05_desafio_chat.py
```

> 💡 Leia os comentários dentro de cada arquivo antes de rodar — eles explicam o conceito por trás do código.

---

## 🧠 Conceitos-chave

**Roles da API**

Toda chamada à API é uma lista de mensagens. Cada mensagem tem um papel:

| Role        | Para que serve                                       |
|-------------|------------------------------------------------------|
| `system`    | Define o comportamento e personagem do modelo        |
| `user`      | A mensagem que você envia                            |
| `assistant` | A resposta do modelo (usada para montar o histórico) |

**Tokens**

Modelos não leem palavras — leem tokens. Um token equivale a aproximadamente 0,75 palavras em inglês ou 0,5 palavras em português. Tokens determinam o custo e o limite de contexto de cada chamada.

**Stateless e memória**

LLMs não têm memória entre chamadas. Para simular uma conversa contínua, você envia o histórico completo a cada nova mensagem — é exatamente o que o arquivo `04_memoria_conversa.py` demonstra.

**Variável MODEL no .env**

O modelo usado nas chamadas é lido do arquivo `.env` via `os.getenv("MODEL")`. Isso permite trocar o modelo sem tocar no código — basta alterar uma linha no `.env`. O valor padrão `openrouter/free` garante que apenas modelos 100% gratuitos sejam usados.

---

## ✅ Checklist de conclusão

Antes de avançar para o próximo módulo, confirme que você conseguiu:

- [ ] Rodar o `01_setup.py` sem erros
- [ ] Ver uma resposta real do modelo no `02_primeira_chamada.py`
- [ ] Entender a diferença entre os três system prompts do `03_funcao_reutilizavel.py`
- [ ] Observar o modelo "lembrando" o nome no `04_memoria_conversa.py`
- [ ] Ter uma conversa completa pelo terminal no `05_desafio_chat.py`

---

## ➡️ Próximo módulo

[Módulo 2 — Machine Learning](../modulo2_ml/README.md)