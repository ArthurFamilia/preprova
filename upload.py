import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_pdf():
    st.title("Upload de Arquivo PDF")

    uploaded_file = st.file_uploader("Selecione um arquivo PDF", type="pdf")
    
    if uploaded_file:
        if uploaded_file.size > 10 * 1024 * 1024:  # Limite de 10MB
            st.error("O arquivo excede o tamanho máximo permitido (10MB).")
            return

        with st.spinner("Carregando PDF..."):
            # Envia para o Supabase Storage
            storage_response = supabase.storage.from_("pdfs").upload(f"{uploaded_file.name}", uploaded_file)
            
            if not storage_response:
                st.error("Erro ao fazer upload do arquivo.")
                return

            # Obtém URL do arquivo
            pdf_url = f"{SUPABASE_URL}/storage/v1/object/public/pdfs/{uploaded_file.name}"

            # Cria uma pré-prova vinculada ao usuário logado
            user = supabase.auth.get_user()
            if user:
                user_id = user.user.id
                response = supabase.table("preprovas").insert({"user_id": user_id, "pdf_url": pdf_url}).execute()

                if response.data:
                    st.success("PDF carregado com sucesso! Agora gere sua pré-prova.")
                    st.session_state["preprova_id"] = response.data[0]["id"]
                    st.experimental_rerun()
                else:
                    st.error("Erro ao criar pré-prova.")
            else:
                st.error("Usuário não autenticado.")

