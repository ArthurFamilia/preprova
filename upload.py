import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
import generate_questions  # Importa a função de geração de questões
import io

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_pdf():
    st.title("Upload de Arquivo PDF")

    uploaded_file = st.file_uploader("Selecione um arquivo PDF", type="pdf")
    
    if uploaded_file:
        if uploaded_file.size > 10 * 1024 * 1024:  # Limite de 10MB
            st.error("O arquivo excede o tamanho máximo permitido (10MB).")
            return

        with st.spinner("Carregando PDF..."):
            # 🔹 Converte o arquivo para um formato correto antes do upload
            file_bytes = io.BytesIO(uploaded_file.getvalue())  # Converte para um stream de bytes

            try:
                # Envia para o Supabase Storage
                storage_response = supabase.storage.from_("pdfs").upload(uploaded_file.name, file_bytes, {"content-type": "application/pdf"})
            
                if not storage_response:
                    st.error("Erro ao fazer upload do arquivo. Verifique se o bucket existe e se há permissões suficientes.")
                    return

                # Obtém URL do arquivo
                pdf_url = f"{SUPABASE_URL}/storage/v1/object/public/pdfs/{uploaded_file.name}"

                # Cria uma pré-prova vinculada ao usuário logado
                user = supabase.auth.get_user()
                if user:
                    user_id = user.user.id
                    response = supabase.table("preprovas").insert({"user_id": user_id, "pdf_url": pdf_url}).execute()

                    if response.data:
                        preprova_id = response.data[0]["id"]
                        st.session_state["preprova_id"] = preprova_id
                        st.success("PDF carregado com sucesso! Gerando sua pré-prova...")

                        # 🔹 Chama a API da OpenAI para gerar perguntas automaticamente
                        with st.spinner("Gerando questões... Isso pode levar alguns segundos."):
                            success = generate_questions.generate_questions(preprova_id, pdf_url)

                            if success:
                                st.success("Questões geradas com sucesso! Acesse sua pré-prova.")
                                st.rerun()
                            else:
                                st.error("Erro ao gerar questões. Tente novamente.")
                    else:
                        st.error("Erro ao criar pré-prova.")
                else:
                    st.error("Usuário não autenticado.")
            except Exception as e:
                st.error(f"Erro no upload para o Supabase: {str(e)}")
