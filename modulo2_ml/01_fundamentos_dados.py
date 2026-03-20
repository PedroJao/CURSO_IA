# ============================================================
# MÓDULO 2 — MACHINE LEARNING | Arquivo 01: Fundamentos de Dados
# Semana 5 — NumPy, Pandas e Análise Exploratória (EDA)
# ============================================================
# Antes de rodar: uv add numpy pandas matplotlib seaborn
#
# CONCEITO:
# Antes de treinar qualquer modelo de ML, você SEMPRE precisa
# entender seus dados. EDA (Exploratory Data Analysis) é o processo
# de explorar, visualizar e resumir os dados para descobrir padrões,
# anomalias e relações entre variáveis.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("✅ Bibliotecas importadas!\n")

# ── PARTE 1: NumPy — a base matemática do ML ────────────────
print("=" * 55)
print("  📐 PARTE 1: NumPy")
print("=" * 55)

# Arrays são muito mais eficientes que listas Python para ML
lista_python = [1, 2, 3, 4, 5]
array_numpy  = np.array([1, 2, 3, 4, 5])

# Operações matemáticas em arrays acontecem elemento a elemento
print(f"Array original:    {array_numpy}")
print(f"Multiplicado por 2: {array_numpy * 2}")
print(f"Elevado ao quadrado: {array_numpy ** 2}")
print(f"Média:  {array_numpy.mean():.2f}")
print(f"Desvio: {array_numpy.std():.2f}")

# Arrays 2D — como tabelas de dados
matriz = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
print(f"\nMatriz 3x3:\n{matriz}")
print(f"Shape: {matriz.shape}  ← (linhas, colunas)")
print(f"Média por coluna: {matriz.mean(axis=0)}")

# ── PARTE 2: Pandas — manipulação de dados ───────────────────
print("\n" + "=" * 55)
print("  🐼 PARTE 2: Pandas")
print("=" * 55)

# Criando um DataFrame — a estrutura principal do Pandas
dados = {
    "nome":       ["Ana", "Bruno", "Carla", "Diego", "Elena"],
    "idade":      [28, 35, 22, 41, 30],
    "salario":    [4500, 7200, 3100, 9800, 5600],
    "experiencia": [3, 8, 1, 15, 5],
    "aprovado":   [True, True, False, True, True]
}
df = pd.DataFrame(dados)

print("📋 DataFrame criado:")
print(df)

print("\n📊 Estatísticas descritivas:")
print(df.describe().round(2))

print(f"\n🔍 Shape: {df.shape}  ← ({df.shape[0]} linhas, {df.shape[1]} colunas)")
print(f"🔍 Tipos de dados:\n{df.dtypes}")

# Filtragem — selecionando linhas com condições
aprovados = df[df["aprovado"] == True]
print(f"\n✅ Aprovados ({len(aprovados)}):")
print(aprovados[["nome", "salario", "experiencia"]])

# Criando nova coluna calculada
df["salario_por_ano_exp"] = (df["salario"] / df["experiencia"]).round(0)
print(f"\n💰 Salário por ano de experiência:")
print(df[["nome", "salario", "experiencia", "salario_por_ano_exp"]])

# ── PARTE 3: EDA com dados reais ─────────────────────────────
print("\n" + "=" * 55)
print("  🔬 PARTE 3: EDA com Dataset Real (Iris)")
print("=" * 55)

# Dataset Iris — clássico do ML, embutido no seaborn
iris = sns.load_dataset("iris")

print(f"📦 Dataset Iris: {iris.shape[0]} amostras, {iris.shape[1]} colunas")
print(f"\nPrimeiras linhas:")
print(iris.head())

print(f"\nEspécies disponíveis: {iris['species'].unique()}")
print(f"\nDistribuição:\n{iris['species'].value_counts()}")

print(f"\nValores nulos:\n{iris.isnull().sum()}")
# Nenhum! Iris é um dataset limpo — no mundo real raramente é assim

print(f"\nEstatísticas por espécie:")
print(iris.groupby("species")[["petal_length", "petal_width"]].mean().round(2))

# ── PARTE 4: Visualizações ────────────────────────────────────
print("\n📈 Gerando visualizações...")

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("EDA — Dataset Iris", fontsize=14, fontweight="bold")

# Gráfico 1: distribuição das espécies
iris["species"].value_counts().plot(kind="bar", ax=axes[0],
    color=["#4C72B0", "#DD8452", "#55A868"], edgecolor="white")
axes[0].set_title("Distribuição das Espécies")
axes[0].set_xlabel("Espécie")
axes[0].set_ylabel("Quantidade")
axes[0].tick_params(axis="x", rotation=0)

# Gráfico 2: correlação entre features
corr = iris.drop(columns="species").corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues",
            ax=axes[1], square=True)
axes[1].set_title("Correlação entre Features")

# Gráfico 3: dispersão petal_length vs petal_width
for especie, cor in zip(iris["species"].unique(),
                        ["#4C72B0", "#DD8452", "#55A868"]):
    subset = iris[iris["species"] == especie]
    axes[2].scatter(subset["petal_length"], subset["petal_width"],
                    label=especie, color=cor, alpha=0.7)
axes[2].set_xlabel("Comprimento da Pétala")
axes[2].set_ylabel("Largura da Pétala")
axes[2].set_title("Pétala: Comprimento vs Largura")
axes[2].legend()

plt.tight_layout()
plt.savefig("modulo2_ml/eda_iris.png", dpi=100, bbox_inches="tight")
plt.show()
print("💾 Gráfico salvo em modulo2_ml/eda_iris.png")

# ── RESUMO ───────────────────────────────────────────────────
print("\n" + "=" * 55)
print("✅ RESUMO DO ARQUIVO 01")
print("=" * 55)
print("""
O que você aprendeu:
  • NumPy: arrays eficientes, operações matemáticas vetorizadas
  • Pandas: DataFrames, filtragem, colunas calculadas
  • EDA: shape, describe, value_counts, isnull, groupby
  • Visualização: bar chart, heatmap, scatter plot

Próximo arquivo: 02_algoritmos_supervisionados.py
  → Treinar seus primeiros modelos de ML!
""")