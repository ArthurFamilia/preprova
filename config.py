import os

# Carregando credenciais do ambiente (Streamlit Secrets)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
DB_PASSWORD = os.getenv("DB_PASSWORD")
OPENAI_KEY = os.getenv("OPENAI_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Erro: SUPABASE_URL ou SUPABASE_KEY não estão configurados corretamente.")

if not OPENAI_KEY:
    raise ValueError("Erro: OPENAI_KEY não foi configurado no ambiente do Streamlit.")
