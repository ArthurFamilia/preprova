import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def delete_preprova(preprova_id):
    """Apaga a pré-prova do banco de dados e do armazenamento."""
    try:
        response = supabase.table("preprovas").select("pdf_url").eq("id", preprova_id).execute()
        
        if not response.data:
            st.error("Erro: Pré-prova não encontrada.")
            return

        pdf_url = response.data[0]["pdf_url"]
        file_name = pdf_url.split("/")[-1]  

        supabase.storage.from_("pdfs").remove([file_name])
        supabase.table("questoes").delete().eq("preprova_id", preprova_id).execute()
        supabase.table("preprovas").delete().eq("id", preprova_id).execute()

        # Remove a pré-prova da sessão
        st.session_state["preprovas"] = [p for p in st.session_state.get("preprovas", []) if p["id"] != preprova_id]

        st.success(f"🗑️ Pré-prova {preprova_id} apagada com sucesso!")

    except Exception as e:
        st.error(f"❌ Erro ao apagar a pré-prova: {str(e)}")

def carregar_preprovas():
    """Carrega todas as pré-provas do usuário do banco de dados"""
    user_id = st.session_state.get("user_id")
    if not user_id:
        return []

    response = supabase.table("preprovas").select("*").eq("user_id", user_id).execute()
    return response.data if response.data else []

def preprova_page():
    st.title("Minhas Pré-Provas")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("❌ Usuário não autenticado. Faça login novamente.")
        return

    if "preprovas" not in st.session_state:
        st.session_state["preprovas"] = carregar_preprovas()

    preprovas = st.session_state["preprovas"]

    if not preprovas:
        st.warning("Nenhuma pré-prova encontrada. Faça o upload de um PDF primeiro.")
        return

    for preprova in preprovas:
        with st.expander(f"📄 Pré-Prova {preprova['id']}"):
            st.write(f"📂 PDF: [{preprova['pdf_url']}]({preprova['pdf_url']})")
            
            col1, col2 = st.columns([3, 1])

            with col1:
                if st.button(f"📝 Fazer Quiz", key=f"quiz_btn_{preprova['id']}"):
                    st.session_state["preprova_id"] = preprova["id"]
                    st.session_state["pdf_url"] = preprova["pdf_url"]
                    st.session_state["menu"] = "Quiz"

            with col2:
                if st.button("🗑️ Apagar", key=f"delete_btn_{preprova['id']}"):
                    delete_preprova(preprova["id"])

if __name__ == "__main__":
    preprova_page()
