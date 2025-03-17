import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def delete_preprova(preprova_id):
    """Apaga a pré-prova do banco de dados e do armazenamento."""
    try:
        # Obtém a pré-prova para deletar o arquivo do Supabase Storage
        response = supabase.table("preprovas").select("pdf_url").eq("id", preprova_id).execute()
        
        if not response.data:
            st.error("Erro: Pré-prova não encontrada.")
            return

        pdf_url = response.data[0]["pdf_url"]
        file_name = pdf_url.split("/")[-1]  # Extrai o nome do arquivo do Supabase Storage
        
        # Apaga o arquivo do Supabase Storage
        supabase.storage.from_("pdfs").remove([file_name])

        # Apaga as questões associadas à pré-prova
        supabase.table("questoes").delete().eq("preprova_id", preprova_id).execute()

        # Apaga a pré-prova do banco de dados
        supabase.table("preprovas").delete().eq("id", preprova_id).execute()

        st.success("🗑️ Pré-prova apagada com sucesso!")

    except Exception as e:
        st.error(f"❌ Erro ao apagar a pré-prova: {str(e)}")

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
            
            col1, col2 = st.columns([3, 1])

            with col1:
                if st.button(f"📝 Fazer Quiz {preprova['id']}", key=f"quiz_{preprova['id']}"):
                    st.session_state["preprova_id"] = preprova["id"]
                    st.session_state["pdf_url"] = preprova["pdf_url"]
                    st.session_state["menu"] = "Quiz"
                    st.rerun()
            
            with col2:
                if st.button("🗑️ Apagar", key=f"delete_{preprova['id']}", help="Excluir esta pré-prova permanentemente"):
                    delete_preprova(preprova["id"])
                    st.rerun()

if __name__ == "__main__":
    preprova_page()
