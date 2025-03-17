import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
import login
import home
import upload
import preprova

def init_connection():
    """Inicializa a conexão com o Supabase."""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def main():
    """Gerencia a navegação e autenticação do usuário."""
    st.set_page_config(page_title="Pre Prova Medicina", layout="wide")

    # Inicializa conexão com o Supabase
    supabase = init_connection()
    
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Se não estiver logado, exibir a tela de login
    if not st.session_state["logged_in"]:
        login.login_page()
        return  # Evita que a sidebar apareça antes do login
    
    # Navegação da Sidebar
    st.sidebar.title("Navegação")
    # menu = st.sidebar.radio("Escolha a página", ["Home", "Upload PDF", "Pré-Prova", "Sair"])
    menu = st.sidebar.radio("Escolha a página", ["Home", "Upload PDF", "Pré-Prova", "Sair"], index=["Home", "Upload PDF", "Pré-Prova", "Sair"].index(st.session_state.get("menu", "Home")))


    if menu == "Home":
        home.home_page()
    elif menu == "Upload PDF":
        upload.upload_pdf()
    elif menu == "Pré-Prova":
        preprova.preprova_page()
    elif menu == "Sair":
        st.session_state.clear()
        st.rerun()

if __name__ == "__main__":
    main()
