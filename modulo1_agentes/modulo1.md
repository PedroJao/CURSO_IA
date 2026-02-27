# 🤖 Curso de Inteligência Artificial com Python

Bem-vindo ao curso prático de IA com Python! Este repositório contém todos os módulos, aulas e projetos da trilha completa — do zero até agentes de IA, Machine Learning e Redes Neurais.

---

## 📋 Pré-requisitos

- Computador com Windows 10 ou superior
- Conexão com a internet
- Conta Google (para o OpenRouter)

Não precisa saber Linux nem ter Python instalado — tudo será configurado do zero nos passos abaixo.

---

## 🪟 Passo 1 — Instalar o WSL (Windows Subsystem for Linux)

O WSL permite rodar Linux diretamente no Windows, sem precisar de máquina virtual.

**1.1 — Abra o PowerShell como Administrador**

Clique no botão Iniciar, pesquise por **PowerShell**, clique com o botão direito e selecione **"Executar como administrador"**.

**1.2 — Instale o WSL com Ubuntu**

Cole o comando abaixo e pressione Enter:

```powershell
wsl --install
```

Esse comando instala automaticamente o WSL 2 com o Ubuntu. O processo pode levar alguns minutos.

**1.3 — Reinicie o computador**

Após a instalação, reinicie o computador quando solicitado.

**1.4 — Configure o Ubuntu**

Após reiniciar, o Ubuntu vai abrir automaticamente e pedir para você criar um usuário e senha. Escolha um nome de usuário simples (sem espaços) e uma senha que você lembre — **a senha não aparece na tela enquanto você digita, isso é normal**.

**1.5 — Verifique a instalação**

Abra o Ubuntu pelo menu Iniciar e rode:

```bash
uname -a
```

Se aparecer uma linha com "Linux", o WSL está funcionando corretamente.

> 💡 **Dica:** Para abrir o WSL no futuro, pesquise por "Ubuntu" no menu Iniciar ou abra o Windows Terminal e selecione Ubuntu na seta ao lado das abas.

---

## ⚡ Passo 2 — Instalar o UV (gerenciador de pacotes Python)

O UV é um gerenciador de pacotes e ambientes virtuais para Python. É muito mais rápido que o pip tradicional e cuida automaticamente da versão do Python para você.

**2.1 — Abra o terminal do Ubuntu (WSL)**

**2.2 — Instale o UV**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**2.3 — Recarregue o terminal**

```bash
source $HOME/.local/bin/env
```

**2.4 — Verifique a instalação**

```bash
uv --version
```

Deve aparecer algo como `uv 0.x.x`. Se aparecer, está tudo certo!

> 💡 **O que é o UV?** Diferente do pip, o UV cria ambientes virtuais isolados por projeto, gerencia versões do Python automaticamente e instala pacotes muito mais rápido. Você não precisa instalar o Python separadamente — o UV faz isso por você.

---

## 🔑 Passo 3 — Criar conta e obter a API Key no OpenRouter

O OpenRouter é uma plataforma que dá acesso a dezenas de modelos de IA (incluindo modelos gratuitos) através de uma única API. Vamos usá-lo para fazer nossas primeiras chamadas a LLMs sem gastar nada.

**3.1 — Criar a conta**

1. Acesse **openrouter.ai**
2. Clique em **"Sign In"** no canto superior direito
3. Escolha **"Continue with Google"** (ou crie uma conta com e-mail)
4. Siga os passos de autenticação

**3.2 — Acessar a área de API Keys**

1. Após fazer login, clique no seu avatar/foto no canto superior direito
2. Clique em **"Keys"** no menu que aparecer
3. Você verá a tela de gerenciamento de chaves

**3.3 — Criar uma nova API Key**

1. Clique no botão **"Create Key"**
2. Dê um nome para identificar a chave, por exemplo: `curso-ia-python`
3. Clique em **"Create"**
4. **Copie a chave gerada** — ela começa com `sk-or-v1-...`

> ⚠️ **IMPORTANTE:** A chave só é exibida uma vez. Copie e guarde em local seguro antes de fechar a janela. Se perder, será necessário criar uma nova.

**3.4 — Verificar os créditos gratuitos**

O OpenRouter oferece créditos gratuitos para novos usuários, suficientes para todo o Módulo 1. Para verificar:

1. Clique no seu avatar novamente
2. Acesse **"Credits"**
3. Você verá o saldo disponível

> 💡 **Modelos gratuitos:** Durante o curso usamos `openrouter/auto` — um roteador especial que seleciona automaticamente um modelo gratuito disponível no momento. Isso evita erros por modelos descontinuados ou com limite atingido. Você pode conferir todos os modelos gratuitos disponíveis em **openrouter.ai/models** filtrando por "Free".

---

## 📁 Passo 4 — Configurar o Projeto

Com o WSL, UV e API Key prontos, vamos clonar o repositório e configurar o ambiente.

**4.1 — Clone o repositório**

```bash
git clone https://github.com/PedroJao/CURSO_IA.git
cd CURSO_IA
```

**4.2 — Inicialize o projeto com UV**

```bash
uv init
```

Isso cria os arquivos base do projeto, incluindo o `pyproject.toml` que gerencia as dependências.

**4.3 — Crie o arquivo `.env` a partir do exemplo**

O repositório contém um arquivo `.env.example` com o formato correto. Copie-o e preencha com sua chave:

```bash
cp .env.example .env
nano .env
```

Dentro do nano, substitua `sk-or-v1-SUA_CHAVE_AQUI` pela chave que você copiou no Passo 3. Salve com `Ctrl+O`, Enter, e saia com `Ctrl+X`.

O arquivo `.env` final deve ficar assim:
```
OPENROUTER_API_KEY=sk-or-v1-...sua chave real aqui...
```

> ⚠️ **IMPORTANTE:** O `.env` já está no `.gitignore` e nunca será enviado ao GitHub. O `.env.example` é seguro de subir pois não contém nenhuma chave real — serve apenas como modelo.

**4.4 — Instale as dependências do Módulo 1**

```bash
uv add openai python-dotenv
```

O UV vai baixar e instalar tudo automaticamente, incluindo a versão correta do Python.

**4.5 — Estrutura final do projeto**

Após o setup, sua pasta deve estar assim:

```
CURSO_IA/
├── .env                  ← sua chave de API (nunca suba pro GitHub!)
├── .env.example          ← modelo seguro para referência ✅
├── .gitignore            ← protege o .env e outros arquivos
├── pyproject.toml        ← dependências gerenciadas pelo UV
├── modulo1_agentes/
│   ├── README.md
│   ├── 01_setup.py
│   ├── 02_primeira_chamada.py
│   ├── 03_funcao_reutilizavel.py
│   ├── 04_memoria_conversa.py
│   └── 05_desafio_chat.py
├── modulo2_ml/           ← será preenchido no Módulo 2 (Futuramente)
├── modulo3_prompt_eng/   ← será preenchido no Módulo 3 (Futuramente)
└── ...
```

---

## 🚀 Passo 5 — Rodar o Módulo 1

Com tudo configurado, rode os arquivos na ordem abaixo. Cada arquivo é independente e ensina um conceito novo:

```bash
# Comece aqui — verifica se o ambiente está correto
uv run modulo1_agentes/01_setup.py

# Primeira chamada real a um LLM
uv run modulo1_agentes/02_primeira_chamada.py

# Boas práticas com funções reutilizáveis
uv run modulo1_agentes/03_funcao_reutilizavel.py

# Como LLMs simulam memória com histórico
uv run modulo1_agentes/04_memoria_conversa.py

# Projeto final: chat interativo no terminal
uv run modulo1_agentes/05_desafio_chat.py
```

> 💡 **Dica:** Leia os comentários dentro de cada arquivo antes de rodar. Eles explicam o conceito por trás do código.

---

## ❓ Solução de Problemas Comuns

**"comando não encontrado: uv"**
```bash
source $HOME/.local/bin/env
```
Se não resolver, feche e abra o terminal novamente.

**"OPENROUTER_API_KEY não encontrada"**

Verifique se o arquivo `.env` está na raiz do projeto (`curso-ia/`) e se a chave está no formato correto:
```
OPENROUTER_API_KEY=sk-or-v1-...
```
Sem espaços antes ou depois do `=`.

**"ModuleNotFoundError: No module named 'openai'"**

As dependências não foram instaladas. Rode:
```bash
uv add openai python-dotenv
```

**"AuthenticationError" ou erro 401**

Sua chave de API está incorreta ou expirou. Volte ao OpenRouter, crie uma nova chave e atualize o `.env`.

**"RateLimitError" ou erro 429**

Você atingiu o limite do modelo gratuito. Aguarde alguns minutos e tente novamente.

**"NotFoundError" ou erro 404 — "No endpoints found for..."**

O modelo especificado foi descontinuado ou removido do OpenRouter. Abra o arquivo que falhou e troque a linha `MODEL` por:
```python
MODEL = "openrouter/auto"
```
O `openrouter/auto` roteia automaticamente para um modelo gratuito disponível no momento, evitando esse problema no futuro.

**"APIStatusError" ou erro 402 — "USD spend limit exceeded"**

O modelo escolhido está passando por um provedor com limite de gasto atingido. A solução é a mesma do erro 404 — use `openrouter/auto`:
```python
MODEL = "openrouter/auto"
```

**"BadRequestError" ou erro 400 — "is not a valid model ID"**

O valor da variável `MODEL` está incorreto. Verifique se a linha no arquivo está exatamente assim, sem caracteres extras:
```python
MODEL = "openrouter/auto"
```

---

## 📚 Estrutura Completa do Curso

| Módulo | Tema                    | Semanas | Status        |
|--------|-------------------------|---------|---------------|
| 1      | Fundação — LLMs e APIs  | 1-4     | ✅ Disponível  |
| 2      | Machine Learning        | 5-9     | 🔜 Em breve   |
| 3      | Prompt Engineering      | 10-13   | 🔜 Em breve   |
| 4      | Ferramentas e Memória   | 14-17   | 🔜 Em breve   |
| 5      | Frameworks de Agentes   | 18-21   | 🔜 Em breve   |
| 6      | Redes Neurais           | 22-29   | 🔜 Em breve   |
| 7      | Projeto Final           | 30-33   | 🔜 Em breve   |

---
