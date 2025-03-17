import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
import login
import home
import upload
import preprova
import quiz  # Novo módulo de quiz

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
    menu = st.sidebar.radio("Escolha a página", ["Home", "Upload PDF", "Pré-Prova", "Quiz", "Sair"])

    if menu == "Home":
        home.home_page()
    elif menu == "Upload PDF":
        upload.upload_pdf()
    elif menu == "Pré-Prova":
        preprova.preprova_page()
    elif menu == "Quiz":
        quiz.quiz_page()
    elif menu == "Sair":
        st.session_state.clear()
        st.rerun()

if __name__ == "__main__":
    main()
