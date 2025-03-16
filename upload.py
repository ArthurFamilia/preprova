import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
import generate_questions  # Importa a função de geração de questões
import time

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_pdf():
    st.title("Upload de Arquivo PDF")

    # 🔹 Obtém o usuário autenticado da sessão
    user_id = st.session_state.get("user_id")

    if not user_id:
        st.error("Usuário não autenticado. Faça login novamente.")
        return

    # 🔹 Log de depuração do usuário logado
    st.write("Debug User:", user_id)

    uploaded_file = st.file_uploader("Selecione um arquivo PDF", type="pdf")
    
    if uploaded_file:
        if uploaded_file.size > 10 * 1024 * 1024:  # Limite de 10MB
            st.error("O arquivo excede o tamanho máximo permitido (10MB).")
            return

        with st.spinner("Carregando PDF..."):
            try:
                # 🔹 Nome do arquivo com timestamp para evitar conflitos
                timestamp = int(time.time())  
                file_path = f"pdfs/{timestamp}_{uploaded_file.name}"

                # Lê o arquivo como bytes
                file_bytes = uploaded_file.getvalue()

                # 🔹 Faz o upload para o Supabase Storage
                storage_response = supabase.storage.from_("pdfs").upload(file_path, file_bytes)

                if not storage_response:
                    st.error("Erro ao fazer upload do arquivo. Verifique se o bucket existe e se há permissões suficientes.")
                    return

                # Obtém URL do arquivo
                pdf_url = f"{SUPABASE_URL}/storage/v1/object/public/{file_path}"

                # 🔹 Criar uma pré-prova vinculada ao usuário logado
                response = supabase.table("preprovas").insert({"user_id": user_id, "pdf_url": pdf_url}).execute()

                if response.data:
                    preprova_id = response.data[0]["id"]
                    st.session_state["preprova_id"] = preprova_id
                    st.success("✅ PDF carregado com sucesso! Gerando sua pré-prova...")

                    # 🔹 Chama a API da OpenAI para gerar perguntas automaticamente
                    with st.spinner("📝 Gerando questões... Isso pode levar alguns segundos."):
                        success = generate_questions.generate_questions(preprova_id, pdf_url)

                        if success:
                            st.success("🎉 Questões geradas com sucesso! Acesse sua pré-prova.")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao gerar questões. Tente novamente.")
                else:
                    st.error("❌ Erro ao criar pré-prova no banco de dados.")
            except Exception as e:
                st.error(f"❌ Erro no upload para o Supabase: {str(e)}")
