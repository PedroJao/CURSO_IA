# ============================================================
# MÓDULO 2 — MACHINE LEARNING | Arquivo 02: Algoritmos Supervisionados
# Semana 6 — Regressão Logística, KNN, Decision Tree
# ============================================================
# Antes de rodar: uv add scikit-learn
#
# CONCEITO:
# Aprendizado supervisionado = treinar um modelo com exemplos
# que já têm a resposta certa. O modelo aprende o padrão e
# generaliza para novos dados que nunca viu.
#
# Dois tipos:
#   Classificação → prever uma CATEGORIA  (spam/não-spam, espécie)
#   Regressão     → prever um NÚMERO      (preço, temperatura)

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report

print("✅ Bibliotecas importadas!\n")

# ── PREPARAÇÃO DOS DADOS ─────────────────────────────────────
iris = sns.load_dataset("iris")

# Separar features (X) e alvo (y)
X = iris.drop(columns="species").values  # matriz de entrada
y = iris["species"].values               # coluna alvo

# Mapeando strings para números (alguns algoritmos precisam)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_num = le.fit_transform(y)  # setosa=0, versicolor=1, virginica=2

print(f"📦 Dados: {X.shape[0]} amostras × {X.shape[1]} features")
print(f"🏷️  Classes: {le.classes_}")

# ── CONCEITO: TRAIN/TEST SPLIT ───────────────────────────────
print("\n" + "=" * 55)
print("  ✂️  Train/Test Split")
print("=" * 55)
print("""
REGRA FUNDAMENTAL: nunca avalie um modelo nos dados de treino!
É como dar a prova para o aluno estudar antes — não mede aprendizado.

train_test_split separa:
  • 80% para TREINO   → o modelo aprende com esses dados
  • 20% para TESTE    → avaliamos com dados que o modelo nunca viu
""")

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y_num, test_size=0.2, random_state=42, stratify=y_num
)
print(f"Treino: {X_treino.shape[0]} amostras")
print(f"Teste:  {X_teste.shape[0]} amostras")

# ── NORMALIZAÇÃO ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("  📏 Normalização com StandardScaler")
print("=" * 55)
print("""
Alguns algoritmos (KNN, Regressão Logística) são sensíveis
à escala das features. Se uma coluna vai de 0 a 1000 e outra
de 0 a 1, o modelo vai "ignorar" a menor.

StandardScaler transforma cada feature para média=0 e desvio=1.

⚠️  IMPORTANTE: fit_transform() APENAS no treino.
               transform() no teste — para não vazar informação!
""")

scaler = StandardScaler()
X_treino_sc = scaler.fit_transform(X_treino)  # aprende a escala
X_teste_sc  = scaler.transform(X_teste)        # aplica a mesma escala

# ── ALGORITMO 1: KNN ─────────────────────────────────────────
print("=" * 55)
print("  🔵 Algoritmo 1: KNN (K-Nearest Neighbors)")
print("=" * 55)
print("""
Ideia: classifica um ponto baseado nos K vizinhos mais próximos.
Simples e intuitivo — sem "treinamento" real, só memoriza os dados.

Hiperparâmetro principal: K (quantos vizinhos considerar)
  K pequeno → mais sensível a ruído (overfitting)
  K grande  → mais suave, pode subajustar (underfitting)
""")

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_treino_sc, y_treino)
y_pred_knn = knn.predict(X_teste_sc)

print(f"Acurácia no teste: {accuracy_score(y_teste, y_pred_knn):.1%}")
print("\nRelatório completo:")
print(classification_report(y_teste, y_pred_knn,
      target_names=le.classes_))

# ── ALGORITMO 2: REGRESSÃO LOGÍSTICA ─────────────────────────
print("=" * 55)
print("  🟢 Algoritmo 2: Regressão Logística")
print("=" * 55)
print("""
Apesar do nome, é um algoritmo de CLASSIFICAÇÃO.
Aprende uma fronteira de decisão linear entre as classes.
Muito eficiente e interpretável — ótimo ponto de partida.
""")

lr = LogisticRegression(max_iter=300, random_state=42)
lr.fit(X_treino_sc, y_treino)
y_pred_lr = lr.predict(X_teste_sc)

print(f"Acurácia no teste: {accuracy_score(y_teste, y_pred_lr):.1%}")
print("\nRelatório completo:")
print(classification_report(y_teste, y_pred_lr,
      target_names=le.classes_))

# ── ALGORITMO 3: DECISION TREE ───────────────────────────────
print("=" * 55)
print("  🟡 Algoritmo 3: Decision Tree (Árvore de Decisão)")
print("=" * 55)
print("""
Aprende uma sequência de regras if/else para classificar.
Vantagem: completamente interpretável — você pode visualizar
e explicar cada decisão que o modelo toma.

Hiperparâmetro principal: max_depth (profundidade da árvore)
  Profunda demais → memoriza o treino (overfitting)
  Rasa demais     → não aprende o suficiente (underfitting)
""")

dt = DecisionTreeClassifier(max_depth=3, random_state=42)
dt.fit(X_treino_sc, y_treino)
y_pred_dt = dt.predict(X_teste_sc)

print(f"Acurácia no teste: {accuracy_score(y_teste, y_pred_dt):.1%}")
print("\nRelatório completo:")
print(classification_report(y_teste, y_pred_dt,
      target_names=le.classes_))

# Visualizar a árvore de decisão
print("\n📊 Gerando visualização da árvore de decisão...")
plt.figure(figsize=(14, 6))
plot_tree(dt, feature_names=iris.columns[:-1],
          class_names=le.classes_, filled=True,
          rounded=True, fontsize=10)
plt.title("Árvore de Decisão — Dataset Iris (max_depth=3)")
plt.tight_layout()
plt.savefig("modulo2_ml/arvore_decisao.png", dpi=100, bbox_inches="tight")
plt.show()
print("💾 Árvore salva em modulo2_ml/arvore_decisao.png")

# ── COMPARAÇÃO FINAL ─────────────────────────────────────────
print("\n" + "=" * 55)
print("  🏆 Comparação dos 3 Algoritmos")
print("=" * 55)

resultados = {
    "KNN (k=5)":           accuracy_score(y_teste, y_pred_knn),
    "Regressão Logística": accuracy_score(y_teste, y_pred_lr),
    "Decision Tree":       accuracy_score(y_teste, y_pred_dt),
}

for nome, acc in sorted(resultados.items(), key=lambda x: x[1], reverse=True):
    barra = "█" * int(acc * 20)
    print(f"  {nome:<22} {barra} {acc:.1%}")

print("""
💡 OBSERVAÇÕES:
  • Todos os 3 tiveram boa performance no Iris (dataset fácil)
  • Em datasets mais complexos as diferenças ficam maiores
  • Nunca escolha um algoritmo só pela acurácia — considere
    velocidade de treino, interpretabilidade e tipo de dados
""")

print("✅ Arquivo 02 concluído!")
print("   Próximo: 03_avaliacao_modelos.py")