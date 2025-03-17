import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def preprova_page():
    st.title("Minhas Pré-Provas")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("❌ Usuário não autenticado. Faça login novamente.")
        return

    # Obtém todas as pré-provas do usuário
    response = supabase.table("preprovas").select("*").eq("user_id", user_id).execute()

    if not response.data:
        st.warning("Nenhuma pré-prova encontrada. Faça o upload de um PDF primeiro.")
        return

    # Lista todas as pré-provas
    for preprova in response.data:
        with st.expander(f"📄 Pré-Prova {preprova['id']}"):
            st.write(f"📂 PDF: [{preprova['pdf_url']}]({preprova['pdf_url']})")
            if st.button(f"Fazer Quiz {preprova['id']}", key=preprova['id']):
                st.session_state["preprova_id"] = preprova["id"]
                st.session_state["pdf_url"] = preprova["pdf_url"]
                st.session_state["menu"] = "Quiz"
                st.experimental_rerun()

if __name__ == "__main__":
    preprova_page()
