import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
import login
import home
import upload
import preprova
import quiz

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

    # 🔹 Definição do estado inicial do menu
    if "menu" not in st.session_state:
        st.session_state["menu"] = "Home"

    # 🔹 Criando um menu bonito com botões
    with st.sidebar:
        st.title(f"👋 Bem-vindo, {st.session_state.get('user_email', 'Usuário')}")
        st.markdown("---")  # Linha divisória estilosa

        if st.button("🏠 Home", key="home_btn"):
            st.session_state["menu"] = "Home"
        if st.button("📤 Upload PDF", key="upload_btn"):
            st.session_state["menu"] = "Upload PDF"
        if st.button("📑 Pré-Prova", key="preprova_btn"):
            st.session_state["menu"] = "Pré-Prova"
        if st.button("📝 Quiz", key="quiz_btn"):
            st.session_state["menu"] = "Quiz"
        if st.button("🚪 Sair", key="logout_btn"):
            st.session_state.clear()
            st.rerun()

    # 🔹 Renderiza a página correta com base na seleção
    if st.session_state["menu"] == "Home":
        home.home_page()
    elif st.session_state["menu"] == "Upload PDF":
        upload.upload_pdf()
    elif st.session_state["menu"] == "Pré-Prova":
        preprova.preprova_page()
    elif st.session_state["menu"] == "Quiz":
        quiz.quiz_page()

if __name__ == "__main__":
    main()
