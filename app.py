import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
import login
import home
import upload
import preprova
import quiz  # Novo módulo do Quiz

def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def main():
    st.set_page_config(page_title="Pre Prova Medicina", layout="wide")

    supabase = init_connection()
    
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login.login_page()
        return  
    
    st.sidebar.title("Navegação")

    # 🔹 Verifica o menu atual para evitar necessidade de duplo clique
    if "menu" not in st.session_state:
        st.session_state["menu"] = "Home"

    # 🔹 Define a nova página ANTES de renderizar
    menu_options = ["Home", "Upload PDF", "Pré-Prova", "Quiz", "Sair"]
    selected_menu = st.sidebar.radio("Escolha a página", menu_options, 
                                     index=menu_options.index(st.session_state["menu"]))

    # 🔹 Atualiza o estado da sessão ANTES de renderizar
    if selected_menu != st.session_state["menu"]:
        st.session_state["menu"] = selected_menu

    # 🔹 Renderiza a página correta
    if st.session_state["menu"] == "Home":
        home.home_page()
    elif st.session_state["menu"] == "Upload PDF":
        upload.upload_pdf()
    elif st.session_state["menu"] == "Pré-Prova":
        preprova.preprova_page()
    elif st.session_state["menu"] == "Quiz":
        quiz.quiz_page()
    elif st.session_state["menu"] == "Sair":
        st.session_state.clear()
        st.rerun()

if __name__ == "__main__":
    main()
