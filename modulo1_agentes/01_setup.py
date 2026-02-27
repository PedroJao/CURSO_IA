from dotenv import load_dotenv
from openai import OpenAI
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

# 
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    print("❌ Chave não encontrada! Verifique seu arquivo .env")
else:
    print("✅ Chave carregada com sucesso!")

# Cria o cliente apontando para o OpenRouter
client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

print("✅ Cliente OpenAI configurado!")
print("🚀 Ambiente pronto para o Módulo 1.")
