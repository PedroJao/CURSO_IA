# 📊 Módulo 2 — Machine Learning

Neste módulo você aprende os fundamentos de Machine Learning — desde manipulação de dados com Pandas até treinar, avaliar e salvar modelos reais. O projeto final usa o famoso dataset Titanic para um pipeline completo do zero ao modelo em produção.

> ⚠️ **Antes de começar:** certifique-se de ter seguido todos os passos do [README principal](../README.md) com o ambiente virtual ativo (`source .venv/bin/activate`).

---

## 🎯 O que você vai aprender

- Manipular dados com NumPy e Pandas
- Fazer análise exploratória (EDA) com visualizações
- Separar dados em treino e teste corretamente
- Treinar e comparar algoritmos de classificação
- Avaliar modelos com métricas além da acurácia
- Usar Cross-Validation para avaliação robusta
- Entender overfitting e underfitting na prática
- Aplicar Random Forest e XGBoost
- Criar um Pipeline profissional do Scikit-learn
- Salvar e carregar modelos com joblib

---

## 📦 Dependências

```bash
uv add numpy pandas matplotlib seaborn scikit-learn xgboost joblib
```

---

## 📂 Arquivos e ordem de execução

| Arquivo                          | Conceito                                        | Semana |
|----------------------------------|-------------------------------------------------|--------|
| `01_fundamentos_dados.py`        | NumPy, Pandas e EDA com visualizações           | 5      |
| `02_algoritmos_supervisionados.py` | KNN, Regressão Logística, Decision Tree       | 6      |
| `03_avaliacao_modelos.py`        | Métricas, Matriz de Confusão, Cross-Validation  | 7      |
| `04_algoritmos_avancados.py`     | Random Forest, XGBoost, Feature Importance      | 8      |
| `05_projeto_pipeline.py`         | 🏁 Projeto final: Pipeline completo com Titanic | 9      |

---

## ▶️ Como rodar

Execute a partir da raiz do projeto (`CURSO_IA/`):

```bash
uv run modulo2_ml/01_fundamentos_dados.py
uv run modulo2_ml/02_algoritmos_supervisionados.py
uv run modulo2_ml/03_avaliacao_modelos.py
uv run modulo2_ml/04_algoritmos_avancados.py
uv run modulo2_ml/05_projeto_pipeline.py
```

> 💡 Cada arquivo gera gráficos salvos na pasta `modulo2_ml/` — abra-os para visualizar os resultados.

---

## 🧠 Conceitos-chave

**O Pipeline de Machine Learning**

Todo projeto de ML segue o mesmo fluxo:

```
Dados brutos → EDA → Limpeza → Features → Treino → Avaliação → Deploy
```

**Supervisionado vs Não-supervisionado**

| Tipo              | Descrição                              | Exemplo               |
|-------------------|----------------------------------------|-----------------------|
| Supervisionado    | Dados com respostas conhecidas         | Spam/não-spam         |
| Não-supervisionado | Dados sem rótulo, descobre padrões    | Segmentação de clientes|

**Train/Test Split — a regra fundamental**

Nunca avalie um modelo nos mesmos dados que usou para treinar. Separe sempre uma parte dos dados que o modelo nunca vai ver durante o treino.

**Métricas de avaliação**

| Métrica   | Quando usar                                      |
|-----------|--------------------------------------------------|
| Acurácia  | Classes balanceadas, visão geral                 |
| Precisão  | Quando falsos positivos são caros (ex: spam)     |
| Recall    | Quando falsos negativos são caros (ex: doenças)  |
| F1-Score  | Equilíbrio entre precisão e recall               |

**Overfitting vs Underfitting**

- **Overfitting** → modelo memorizou o treino, falha no mundo real (score treino >> score teste)
- **Underfitting** → modelo não aprendeu nem o treino (ambos os scores baixos)
- **Ideal** → scores de treino e teste próximos e altos

---

## 📁 Arquivos gerados

Após rodar todos os arquivos, a pasta `modulo2_ml/` conterá:

```
modulo2_ml/
├── eda_iris.png              ← gráficos da análise exploratória
├── arvore_decisao.png        ← visualização da Decision Tree
├── avaliacao_modelos.png     ← matriz de confusão + cross-validation
├── algoritmos_avancados.png  ← feature importance + comparação
├── projeto_titanic.png       ← resultado final do projeto
└── modelo_titanic.pkl        ← modelo salvo pronto para uso
```

---

## ✅ Checklist de conclusão

- [ ] Gerar e entender os 3 gráficos do arquivo 01
- [ ] Entender a diferença entre os 3 algoritmos do arquivo 02
- [ ] Explicar com suas palavras a diferença entre precisão e recall
- [ ] Entender o que é cross-validation e por que é melhor que um único split
- [ ] Identificar overfitting na tabela do arquivo 03
- [ ] Conseguir rodar o projeto Titanic com acurácia acima de 80%
- [ ] Encontrar o arquivo `modelo_titanic.pkl` gerado na pasta

---

## ➡️ Próximo módulo

[Módulo 3 — Prompt Engineering](../modulo3_prompt_eng/modulo3.md)