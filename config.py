import streamlit as st

# Carregando credenciais do ambiente no Streamlit Cloud
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")
DB_PASSWORD = st.secrets.get("DB_PASSWORD", "")
OPENAI_KEY = st.secrets.get("OPENAI_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Erro: SUPABASE_URL ou SUPABASE_KEY não foram encontrados nos Secrets do Streamlit Cloud.")

if not OPENAI_KEY:
    raise ValueError("Erro: OPENAI_KEY não foi configurado nos Secrets do Streamlit Cloud.")
