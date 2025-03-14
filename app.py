import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
import login
import home

def init_connection():
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.error("Erro: SUPABASE_URL e SUPABASE_KEY não foram definidos corretamente.")
        st.stop()
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def main():
    st.set_page_config(page_title="Pre Prova Medicina", layout="wide")
    supabase = init_connection()
    
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    
    if not st.session_state["logged_in"]:
        login.login_page(supabase)
    else:
        home.home_page()

if __name__ == "__main__":
    main()
