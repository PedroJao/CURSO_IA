# 🤖 Curso de Inteligência Artificial com Python

Bem-vindo ao curso prático de IA com Python! Este repositório contém todos os módulos, aulas e projetos da trilha completa — do zero até Agentes de IA, Machine Learning e Redes Neurais.

---

## 🗺️ O que você vai aprender

| Módulo | Tema                   | Semanas | Status       |
|--------|------------------------|---------|--------------|
| 1      | Fundação — LLMs e APIs | 1–4     | ✅ Disponível |
| 2      | Machine Learning       | 5–9     | 🔜 Em breve  |
| 3      | Prompt Engineering     | 10–13   | 🔜 Em breve  |
| 4      | Ferramentas e Memória  | 14–17   | 🔜 Em breve  |
| 5      | Frameworks de Agentes  | 18–21   | 🔜 Em breve  |
| 6      | Redes Neurais          | 22–29   | 🔜 Em breve  |
| 7      | Projeto Final          | 30–33   | 🔜 Em breve  |

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

O OpenRouter dá acesso a dezenas de modelos de IA (incluindo modelos gratuitos) através de uma única API. Vamos usá-lo para fazer as primeiras chamadas a LLMs sem gastar nada.

**3.1 — Criar a conta**

1. Acesse **openrouter.ai**
2. Clique em **"Sign In"** no canto superior direito
3. Escolha **"Continue with Google"** (ou crie uma conta com e-mail)
4. Siga os passos de autenticação

**3.2 — Criar uma nova API Key**

1. Clique no botão **"Create Key"**
2. Dê um nome para identificar a chave, por exemplo: `curso-ia-python`
3. Clique em **"Create"**
4. **Copie a chave gerada** — ela começa com `sk-or-v1-...`

> ⚠️ **IMPORTANTE:** A chave só é exibida uma vez. Copie e guarde em local seguro antes de fechar a janela. Se perder, será necessário criar uma nova.

**3.3 — Verificar os créditos gratuitos**

1. Clique no seu avatar novamente
2. Acesse **"Credits"**
3. Você verá o saldo disponível

> 💡 **Modelos gratuitos:** Durante o curso usamos `openrouter/auto` — um roteador que seleciona automaticamente um modelo gratuito disponível no momento, evitando erros por modelos descontinuados. Você pode ver todos os modelos gratuitos em **openrouter.ai/models** filtrando por "Free".

---

## 📁 Passo 4 — Configurar o Projeto

**4.1 — Clone o repositório**

```bash
git clone https://github.com/PedroJao/CURSO_IA.git
cd CURSO_IA
```

**4.2 — Inicialize o projeto com UV**

```bash
uv init
```

**4.3 — Crie e ative o ambiente virtual**

```bash
uv venv
source .venv/bin/activate
```

Você saberá que o ambiente está ativo quando o terminal mostrar `CURSO_IA` no início da linha:

```
(CURSO_IA) usuario@maquina:~/CURSO_IA$
```

> 💡 **Importante:** sempre que abrir um novo terminal, rode `source .venv/bin/activate` antes de rodar qualquer arquivo do curso.

**4.4 — Crie o arquivo `.env` a partir do exemplo**

```bash
touch .env
cp .env.example .env
```

Substitua `SUA_CHAVE_AQUI` pela sua chave real criada no openrouter.ai.

> ⚠️ O `.env` já está no `.gitignore` e nunca será enviado ao GitHub. O `.env.example` é seguro pois não contém nenhuma chave real.

---

## 🚀 Passo 5 — Começar o Módulo 1

Com o ambiente configurado, abra a pasta do primeiro módulo

`modulo1_agentes`

Dentro dessa pasta, você vai encontrar o `modulo1.md`, a partir dessa documentação você vai dar seus primeiros passos no **Curso de IA**.

---

## ❓ Solução de Problemas Comuns

**"comando não encontrado: uv"**
```bash
source $HOME/.local/bin/env
```
Se não resolver, feche e abra o terminal novamente.

**"OPENROUTER_API_KEY não encontrada"**

Verifique se o arquivo `.env` está na raiz do projeto e se a chave está no formato correto, sem espaços antes ou depois do `=`:
```
OPENROUTER_API_KEY=sk-or-v1-...
```

**"ModuleNotFoundError: No module named 'openai'"**

O ambiente virtual não está ativo ou as dependências não foram instaladas:
```bash
source .venv/bin/activate
uv add openai python-dotenv
```

**"AuthenticationError" ou erro 401**

Chave de API incorreta ou expirada. Crie uma nova no OpenRouter e atualize o `.env`.

**"RateLimitError" ou erro 429**

Limite do modelo gratuito atingido. Aguarde alguns minutos e tente novamente.

**"NotFoundError" ou erro 404 — "No endpoints found for..."**

O modelo foi descontinuado no OpenRouter. Abra o arquivo que falhou e troque:
```python
MODEL = "openrouter/auto"
```

**"APIStatusError" ou erro 402 — "USD spend limit exceeded"**

Provedor com limite de gasto atingido. Use `openrouter/auto` como solução:
```python
MODEL = "openrouter/auto"
```

**"BadRequestError" ou erro 400 — "is not a valid model ID"**

O valor da variável `MODEL` está incorreto. Verifique se está exatamente assim, sem caracteres extras:
```python
MODEL = "openrouter/auto"
```



