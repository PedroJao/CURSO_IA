# ============================================================
# MÓDULO 2 — MACHINE LEARNING | Arquivo 05: Projeto Final
# Semana 9 — Pipeline Completo com Dataset Titanic
# ============================================================
#
# PROJETO: Prever quais passageiros sobreviveram ao Titanic.
#
# Este arquivo percorre o pipeline completo de ML profissional:
#   1. Carregamento e exploração dos dados
#   2. Limpeza e tratamento de valores nulos
#   3. Feature Engineering (criar novas features)
#   4. Pipeline Scikit-learn (pré-processamento + modelo)
#   5. Avaliação final e salvamento do modelo
#
# Dataset: Titanic (via URL pública, sem precisar do Kaggle)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay, confusion_matrix

print("=" * 55)
print("  🚢 PROJETO FINAL — Titanic Survival Prediction")
print("=" * 55)

# ── ETAPA 1: Carregar e explorar os dados ────────────────────
print("\n📥 Etapa 1: Carregando dados...")

URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

try:
    df = pd.read_csv(URL)
    print(f"✅ Dataset carregado: {df.shape[0]} passageiros, {df.shape[1]} colunas")
except Exception as e:
    print(f"❌ Erro ao carregar: {e}")
    print("Verifique sua conexão com a internet.")
    exit()

print(f"\nPrimeiras linhas:")
print(df[["Name", "Survived", "Pclass", "Sex", "Age", "Fare"]].head())

print(f"\nTaxa de sobrevivência geral: {df['Survived'].mean():.1%}")
print(f"\nSobrevivência por sexo:")
print(df.groupby("Sex")["Survived"].mean().round(3))
print(f"\nSobrevivência por classe:")
print(df.groupby("Pclass")["Survived"].mean().round(3))

print(f"\nValores nulos:")
nulos = df.isnull().sum()
print(nulos[nulos > 0])

# ── ETAPA 2: Limpeza e Feature Engineering ───────────────────
print("\n🔧 Etapa 2: Limpeza e Feature Engineering...")

df_clean = df.copy()

# Tratar valores nulos
df_clean["Age"].fillna(df_clean["Age"].median(), inplace=True)
df_clean["Embarked"].fillna(df_clean["Embarked"].mode()[0], inplace=True)
df_clean.drop(columns=["Cabin"], inplace=True)  # >70% nulo, descartamos

# Feature Engineering — criar novas features com significado
df_clean["FamilySize"] = df_clean["SibSp"] + df_clean["Parch"] + 1
df_clean["IsAlone"] = (df_clean["FamilySize"] == 1).astype(int)

# Extrair título do nome (Mr, Mrs, Miss, Master...)
df_clean["Title"] = df_clean["Name"].str.extract(r",\s*([^\.]+)\.")
titulos_raros = df_clean["Title"].value_counts()
titulos_raros = titulos_raros[titulos_raros < 10].index
df_clean["Title"] = df_clean["Title"].replace(titulos_raros, "Rare")

# Faixa etária
df_clean["AgeBin"] = pd.cut(df_clean["Age"],
    bins=[0, 12, 18, 35, 60, 100],
    labels=["Criança", "Adolescente", "Adulto", "MeiaIdade", "Idoso"])

print(f"✅ Features criadas: FamilySize, IsAlone, Title, AgeBin")
print(f"\nDistribuição de títulos:")
print(df_clean["Title"].value_counts())

# ── ETAPA 3: Preparação para o modelo ───────────────────────
print("\n⚙️  Etapa 3: Preparando features para o modelo...")

# Codificar variáveis categóricas
le_sex  = LabelEncoder()
le_emb  = LabelEncoder()
le_title = LabelEncoder()
le_age  = LabelEncoder()

df_clean["Sex_enc"]      = le_sex.fit_transform(df_clean["Sex"])
df_clean["Embarked_enc"] = le_emb.fit_transform(df_clean["Embarked"])
df_clean["Title_enc"]    = le_title.fit_transform(df_clean["Title"])
df_clean["AgeBin_enc"]   = le_age.fit_transform(df_clean["AgeBin"])

# Selecionar features finais
FEATURES = ["Pclass", "Sex_enc", "Age", "Fare", "FamilySize",
            "IsAlone", "Title_enc", "Embarked_enc", "AgeBin_enc"]

X = df_clean[FEATURES].values
y = df_clean["Survived"].values

print(f"✅ Features selecionadas ({len(FEATURES)}): {FEATURES}")

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
print(f"   Treino: {len(X_treino)} | Teste: {len(X_teste)}")

# ── ETAPA 4: Pipeline profissional ────────────────────────────
print("\n🏗️  Etapa 4: Criando Pipeline...")
print("""
Pipeline do Scikit-learn encadeia etapas automaticamente:
  1. StandardScaler  → normaliza os dados
  2. RandomForest    → treina o modelo

Vantagem: o pipeline garante que o scaler é ajustado
APENAS nos dados de treino e aplicado consistentemente.
""")

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("modelo", RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        min_samples_split=5,
        random_state=42
    ))
])

# Cross-Validation antes do treino final
scores_cv = cross_val_score(pipeline, X_treino, y_treino, cv=5, scoring="accuracy")
print(f"Cross-Validation (5 folds): {scores_cv.mean():.3f} ± {scores_cv.std():.3f}")

# Treino final no conjunto completo de treino
pipeline.fit(X_treino, y_treino)

# ── ETAPA 5: Avaliação final ───────────────────────────────────
print("\n📊 Etapa 5: Avaliação final no conjunto de teste...")

y_pred = pipeline.predict(X_teste)
acuracia = accuracy_score(y_teste, y_pred)

print(f"\n🎯 Acurácia final no teste: {acuracia:.1%}")
print("\nRelatório completo:")
print(classification_report(y_teste, y_pred,
      target_names=["Não Sobreviveu", "Sobreviveu"]))

# Visualizações finais
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Titanic — Resultado do Modelo Final", fontsize=13, fontweight="bold")

# Matriz de confusão
cm = confusion_matrix(y_teste, y_pred)
disp = ConfusionMatrixDisplay(cm, display_labels=["Não Sobreviveu", "Sobreviveu"])
disp.plot(ax=axes[0], colorbar=False, cmap="Blues")
axes[0].set_title(f"Matriz de Confusão\nAcurácia: {acuracia:.1%}")

# Feature importance
rf_model = pipeline.named_steps["modelo"]
importancias = pd.Series(rf_model.feature_importances_, index=FEATURES)
importancias.sort_values().plot(kind="barh", ax=axes[1], color="#4C72B0")
axes[1].set_title("Feature Importance")
axes[1].set_xlabel("Importância")

plt.tight_layout()
plt.savefig("modulo2_ml/projeto_titanic.png", dpi=100, bbox_inches="tight")
plt.show()
print("💾 Gráficos salvos em modulo2_ml/projeto_titanic.png")

# ── ETAPA 6: Salvar o modelo ─────────────────────────────────
print("\n💾 Etapa 6: Salvando o modelo...")
joblib.dump(pipeline, "modulo2_ml/modelo_titanic.pkl")
print("✅ Modelo salvo em modulo2_ml/modelo_titanic.pkl")

# Demonstração de uso do modelo salvo
print("\n🔮 Testando modelo salvo com novos passageiros...")
modelo_salvo = joblib.load("modulo2_ml/modelo_titanic.pkl")

novos_passageiros = pd.DataFrame({
    # Pclass Sex_enc Age  Fare  FamilySize IsAlone Title_enc Embarked_enc AgeBin_enc
    "Pclass":       [3,    1,    1  ],
    "Sex_enc":      [1,    0,    1  ],  # 1=male, 0=female
    "Age":          [22,   38,   35 ],
    "Fare":         [7.25, 71.28, 512],
    "FamilySize":   [2,    2,    1  ],
    "IsAlone":      [0,    0,    1  ],
    "Title_enc":    [1,    2,    1  ],  # Mr, Mrs, Mr
    "Embarked_enc": [2,    0,    0  ],
    "AgeBin_enc":   [2,    2,    2  ],
})

predicoes = modelo_salvo.predict(novos_passageiros)
probabilidades = modelo_salvo.predict_proba(novos_passageiros)

perfis = ["Jack (3ª classe, homem, 22)", "Rose (1ª classe, mulher, 38)", "Passageiro VIP (1ª classe, homem, 35)"]
for perfil, pred, prob in zip(perfis, predicoes, probabilidades):
    resultado = "✅ Sobreviveu" if pred == 1 else "❌ Não sobreviveu"
    print(f"  {perfil}: {resultado} (confiança: {prob[pred]:.1%})")

# ── RESUMO FINAL ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("✅ MÓDULO 2 — MACHINE LEARNING CONCLUÍDO!")
print("=" * 55)
print(f"""
O que você dominou neste módulo:
  ✅ NumPy e Pandas para manipulação de dados
  ✅ EDA — análise exploratória com visualizações
  ✅ Train/Test Split e normalização com StandardScaler
  ✅ Algoritmos: KNN, Regressão Logística, Decision Tree
  ✅ Avaliação: acurácia, F1, matriz de confusão
  ✅ Cross-Validation para avaliação robusta
  ✅ Overfitting vs Underfitting
  ✅ Random Forest e XGBoost
  ✅ Feature Engineering no Titanic
  ✅ Pipeline profissional + salvamento com joblib

Acurácia final no Titanic: {acuracia:.1%}

➡️  Próximo: Módulo 3 — Prompt Engineering
""")