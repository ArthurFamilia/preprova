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

    # 🔹 Inicializa a sessão do menu corretamente
    if "menu" not in st.session_state:
        st.session_state["menu"] = "Home"

    # 🔹 Atualiza o menu apenas quando o usuário escolhe algo diferente
    selected_menu = st.sidebar.radio("Escolha a página", ["Home", "Upload PDF", "Pré-Prova", "Quiz", "Sair"], 
                                     index=["Home", "Upload PDF", "Pré-Prova", "Quiz", "Sair"].index(st.session_state["menu"]))

    if selected_menu != st.session_state["menu"]:
        st.session_state["menu"] = selected_menu
        st.experimental_rerun()  # 🔹 Garante a atualização imediata da interface

    # 🔹 Renderiza a página correta imediatamente
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
