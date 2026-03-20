# ============================================================
# MÓDULO 2 — MACHINE LEARNING | Arquivo 03: Avaliação de Modelos
# Semana 7 — Cross-validation, Métricas e Matriz de Confusão
# ============================================================
#
# CONCEITO:
# Acurácia sozinha não conta a história completa.
# Um modelo pode ter 95% de acurácia e ainda ser inútil —
# imagine um dataset com 95% de uma classe e 5% de outra:
# um modelo que sempre chuta a classe majoritária já tem 95%!
#
# Neste arquivo você aprende a avaliar modelos de forma robusta.

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                              f1_score, confusion_matrix, classification_report,
                              ConfusionMatrixDisplay)

print("✅ Bibliotecas importadas!\n")

# Preparação dos dados
iris = sns.load_dataset("iris")
X = iris.drop(columns="species").values
le = LabelEncoder()
y = le.fit_transform(iris["species"].values)

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
scaler = StandardScaler()
X_treino_sc = scaler.fit_transform(X_treino)
X_teste_sc  = scaler.transform(X_teste)

# ── PARTE 1: Métricas além da Acurácia ───────────────────────
print("=" * 55)
print("  📊 PARTE 1: Métricas de Classificação")
print("=" * 55)
print("""
ACURÁCIA    → % de acertos totais. Enganosa em dados desbalanceados.

PRECISÃO    → Dos que o modelo disse SIM, quantos eram realmente SIM?
              "Quando ele acusa, ele acerta?"

RECALL      → Dos que eram realmente SIM, quantos o modelo encontrou?
              "Ele está deixando passar casos positivos?"

F1-SCORE    → Média harmônica entre precisão e recall.
              Útil quando você precisa equilibrar os dois.

Exemplo clássico:
  Detector de câncer → prefira alto RECALL (não deixar doentes passarem)
  Filtro de spam     → prefira alta PRECISÃO (não bloquear e-mails legítimos)
""")

modelo = LogisticRegression(max_iter=300, random_state=42)
modelo.fit(X_treino_sc, y_treino)
y_pred = modelo.predict(X_teste_sc)

print(f"Acurácia:  {accuracy_score(y_teste, y_pred):.3f}")
print(f"Precisão:  {precision_score(y_teste, y_pred, average='weighted'):.3f}")
print(f"Recall:    {recall_score(y_teste, y_pred, average='weighted'):.3f}")
print(f"F1-Score:  {f1_score(y_teste, y_pred, average='weighted'):.3f}")

# ── PARTE 2: Matriz de Confusão ──────────────────────────────
print("\n" + "=" * 55)
print("  🔲 PARTE 2: Matriz de Confusão")
print("=" * 55)
print("""
A matriz de confusão mostra ONDE o modelo erra:
  • Linha = classe real
  • Coluna = classe prevista
  • Diagonal principal = acertos
  • Fora da diagonal = erros e com qual classe confundiu
""")

cm = confusion_matrix(y_teste, y_pred)
print("Matriz de confusão (números):")
print(cm)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Visualização da matriz
disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                               display_labels=le.classes_)
disp.plot(ax=axes[0], colorbar=False, cmap="Blues")
axes[0].set_title("Matriz de Confusão\nRegressão Logística")

# ── PARTE 3: Cross-Validation ────────────────────────────────
print("=" * 55)
print("  🔄 PARTE 3: Cross-Validation (Validação Cruzada)")
print("=" * 55)
print("""
Um único split treino/teste pode ser "sortudo" ou "azarado".
Cross-Validation resolve isso: divide os dados em K partes (folds),
treina K vezes — cada vez usando uma parte diferente como teste.

Resultado: K scores → média e desvio padrão = avaliação robusta.

     Fold 1: [TESTE][TREINO][TREINO][TREINO][TREINO]
     Fold 2: [TREINO][TESTE][TREINO][TREINO][TREINO]
     Fold 3: [TREINO][TREINO][TESTE][TREINO][TREINO]
     Fold 4: [TREINO][TREINO][TREINO][TESTE][TREINO]
     Fold 5: [TREINO][TREINO][TREINO][TREINO][TESTE]
""")

algoritmos = {
    "KNN":               KNeighborsClassifier(n_neighbors=5),
    "Regressão Log.":    LogisticRegression(max_iter=300, random_state=42),
    "Decision Tree":     DecisionTreeClassifier(max_depth=3, random_state=42),
    "Random Forest":     RandomForestClassifier(n_estimators=100, random_state=42),
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
resultados = {}

print(f"{'Algoritmo':<22} {'Média':>8} {'Desvio':>8} {'Min':>7} {'Max':>7}")
print("-" * 55)

for nome, alg in algoritmos.items():
    scores = cross_val_score(alg, X_treino_sc, y_treino, cv=cv, scoring="accuracy")
    resultados[nome] = scores
    print(f"{nome:<22} {scores.mean():>8.3f} {scores.std():>8.3f} "
          f"{scores.min():>7.3f} {scores.max():>7.3f}")

# Boxplot dos resultados
axes[1].boxplot(resultados.values(), labels=resultados.keys(), vert=True)
axes[1].set_title("Cross-Validation (5 folds)\nDistribuição de Acurácia")
axes[1].set_ylabel("Acurácia")
axes[1].tick_params(axis="x", rotation=15)
axes[1].grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("modulo2_ml/avaliacao_modelos.png", dpi=100, bbox_inches="tight")
plt.show()
print("\n💾 Gráficos salvos em modulo2_ml/avaliacao_modelos.png")

# ── PARTE 4: Overfitting vs Underfitting ─────────────────────
print("\n" + "=" * 55)
print("  ⚖️  PARTE 4: Overfitting vs Underfitting")
print("=" * 55)
print("""
OVERFITTING  → modelo memorizou o treino mas falha no teste
               Score treino muito alto, score teste bem menor

UNDERFITTING → modelo não aprendeu nem o treino
               Score treino e teste ambos baixos

IDEAL        → score treino e teste próximos e altos
""")

print(f"{'max_depth':<12} {'Treino':>8} {'Teste':>8} {'Diferença':>12} {'Diagnóstico'}")
print("-" * 60)

for depth in [1, 2, 3, 5, 10, None]:
    dt = DecisionTreeClassifier(max_depth=depth, random_state=42)
    dt.fit(X_treino_sc, y_treino)
    score_treino = dt.score(X_treino_sc, y_treino)
    score_teste  = dt.score(X_teste_sc, y_teste)
    diff = score_treino - score_teste
    label = str(depth) if depth else "None (sem limite)"

    if diff > 0.05:
        diagnostico = "⚠️  Overfitting"
    elif score_treino < 0.85:
        diagnostico = "📉 Underfitting"
    else:
        diagnostico = "✅ Bom equilíbrio"

    print(f"{label:<12} {score_treino:>8.3f} {score_teste:>8.3f} "
          f"{diff:>12.3f} {diagnostico}")

print("""
💡 CONCLUSÃO:
  max_depth=3 oferece o melhor equilíbrio para o Iris.
  Árvores sem limite de profundidade memorizam o treino!
""")

print("✅ Arquivo 03 concluído!")
print("   Próximo: 04_algoritmos_avancados.py")