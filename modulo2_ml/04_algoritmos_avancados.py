# ============================================================
# MÓDULO 2 — MACHINE LEARNING | Arquivo 04: Algoritmos Avançados
# Semana 8 — Random Forest, XGBoost e Feature Importance
# ============================================================
# Antes de rodar: uv add xgboost
#
# CONCEITO:
# Random Forest e XGBoost são os algoritmos mais usados em
# competições e produção para dados tabulares. Ambos são
# baseados em "ensemble" — combinam vários modelos fracos
# para criar um modelo forte.

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

print("✅ Bibliotecas importadas!\n")

# Preparação dos dados
iris = sns.load_dataset("iris")
X = iris.drop(columns="species").values
le = LabelEncoder()
y = le.fit_transform(iris["species"].values)
feature_names = iris.columns[:-1].tolist()

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
scaler = StandardScaler()
X_treino_sc = scaler.fit_transform(X_treino)
X_teste_sc  = scaler.transform(X_teste)

# ── PARTE 1: Random Forest ────────────────────────────────────
print("=" * 55)
print("  🌲 PARTE 1: Random Forest")
print("=" * 55)
print("""
IDEIA: em vez de uma única Decision Tree, treinamos MUITAS
árvores (a "floresta") — cada uma em uma amostra aleatória
dos dados e das features. A decisão final é por votação.

Por que funciona melhor que uma árvore só?
  • Cada árvore erra de formas diferentes
  • Quando combinamos, os erros se cancelam
  • Muito difícil de fazer overfitting

Hiperparâmetros principais:
  n_estimators → quantas árvores (mais = melhor, mas mais lento)
  max_depth    → profundidade de cada árvore
  max_features → quantas features considerar em cada split
""")

# Comparando Decision Tree vs Random Forest
dt = DecisionTreeClassifier(max_depth=3, random_state=42)
rf = RandomForestClassifier(n_estimators=100, random_state=42)

dt.fit(X_treino_sc, y_treino)
rf.fit(X_treino_sc, y_treino)

print(f"Decision Tree  — Teste: {dt.score(X_teste_sc, y_teste):.3f} | "
      f"Treino: {dt.score(X_treino_sc, y_treino):.3f}")
print(f"Random Forest  — Teste: {rf.score(X_teste_sc, y_teste):.3f} | "
      f"Treino: {rf.score(X_treino_sc, y_treino):.3f}")

# ── PARTE 2: Feature Importance ──────────────────────────────
print("\n" + "=" * 55)
print("  🎯 PARTE 2: Feature Importance")
print("=" * 55)
print("""
Random Forest calcula automaticamente a importância de cada
feature — quanto cada coluna contribuiu para as decisões.

Isso é extremamente útil para:
  • Entender o que realmente importa no seu dataset
  • Remover features irrelevantes (acelera o treino)
  • Explicar o modelo para stakeholders não-técnicos
""")

importancias = pd.Series(rf.feature_importances_, index=feature_names)
importancias_sorted = importancias.sort_values(ascending=True)

print("Importância das features:")
for feat, imp in importancias_sorted.items():
    barra = "█" * int(imp * 40)
    print(f"  {feat:<22} {barra} {imp:.3f}")

# ── PARTE 3: XGBoost ─────────────────────────────────────────
print("\n" + "=" * 55)
print("  ⚡ PARTE 3: XGBoost (Extreme Gradient Boosting)")
print("=" * 55)
print("""
IDEIA: ao contrário do Random Forest (paralelo), o XGBoost
treina árvores em SEQUÊNCIA — cada nova árvore aprende a
corrigir os erros da anterior. Isso é "Gradient Boosting".

XGBoost é a versão otimizada e extremamente eficiente.
É o algoritmo mais premiado em competições do Kaggle para
dados tabulares.

Random Forest vs XGBoost:
  Random Forest → mais robusto, menos hiperparâmetros, mais fácil
  XGBoost       → geralmente mais preciso, mas exige mais tuning
""")

xgb = XGBClassifier(n_estimators=100, max_depth=3,
                     learning_rate=0.1, random_state=42,
                     eval_metric="mlogloss", verbosity=0)
xgb.fit(X_treino_sc, y_treino)

print(f"XGBoost — Teste: {xgb.score(X_teste_sc, y_teste):.3f} | "
      f"Treino: {xgb.score(X_treino_sc, y_treino):.3f}")

# ── PARTE 4: Comparação gráfica ───────────────────────────────
print("\n" + "=" * 55)
print("  🏆 PARTE 4: Comparação Completa com Cross-Validation")
print("=" * 55)

algoritmos = {
    "Decision Tree": DecisionTreeClassifier(max_depth=3, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "XGBoost":       XGBClassifier(n_estimators=100, max_depth=3,
                                    eval_metric="mlogloss", verbosity=0, random_state=42),
}

resultados = {}
print(f"\n{'Algoritmo':<16} {'Média CV':>9} {'Desvio':>8}")
print("-" * 36)

for nome, alg in algoritmos.items():
    scores = cross_val_score(alg, X_treino_sc, y_treino, cv=5, scoring="accuracy")
    resultados[nome] = scores
    print(f"{nome:<16} {scores.mean():>9.3f} {scores.std():>8.3f}")

# Visualizações
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Gráfico 1: Feature Importance
importancias_sorted.plot(kind="barh", ax=axes[0],
    color=["#4C72B0", "#55A868", "#DD8452", "#C44E52"])
axes[0].set_title("Feature Importance — Random Forest")
axes[0].set_xlabel("Importância")

# Gráfico 2: Boxplot Cross-Validation
axes[1].boxplot(resultados.values(), labels=resultados.keys())
axes[1].set_title("Comparação — Cross-Validation (5 folds)")
axes[1].set_ylabel("Acurácia")
axes[1].tick_params(axis="x", rotation=10)
axes[1].grid(axis="y", alpha=0.3)
axes[1].set_ylim([0.85, 1.01])

plt.tight_layout()
plt.savefig("modulo2_ml/algoritmos_avancados.png", dpi=100, bbox_inches="tight")
plt.show()
print("💾 Gráficos salvos em modulo2_ml/algoritmos_avancados.png")

print("""
💡 QUANDO USAR CADA UM:
  Decision Tree  → quando você precisa explicar cada decisão
  Random Forest  → ponto de partida sólido para qualquer problema
  XGBoost        → quando você quer espremer o máximo de performance
""")
print("✅ Arquivo 04 concluído!")
print("   Próximo: 05_projeto_pipeline.py → projeto completo!")