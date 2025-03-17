import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
import generate_questions
import time
import re
import tempfile
from urllib import request

# Inicializa o cliente Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_pdf():
    st.title("Upload de Arquivo PDF")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("❌ Usuário não autenticado. Faça login novamente.")
        return

    uploaded_file = st.file_uploader("Selecione um arquivo PDF", type="pdf")

    if uploaded_file:
        if uploaded_file.size > 10 * 1024 * 1024:
            st.error("O arquivo excede o tamanho máximo permitido (10MB).")
            return

        with st.spinner("Carregando PDF..."):
            try:
                safe_file_name = re.sub(r'\s+', '_', uploaded_file.name)
                safe_file_name = re.sub(r'[^\w\-.]', '', safe_file_name)
                timestamp = int(time.time())
                file_path_in_bucket = f"{timestamp}_{safe_file_name}"
                bucket_name = "pdfs"

                # Salva o arquivo temporariamente
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                    temp_file_path = temp_file.name

                # Faz o upload para o Supabase
                with open(temp_file_path, "rb") as file_data:
                    response = supabase.storage.from_(bucket_name).upload(
                        file_path_in_bucket, file_data, {"content-type": "application/pdf"}
                    )

                if not response:
                    st.error("❌ Erro no upload do arquivo.")
                    return

                pdf_url = f"{SUPABASE_URL}/storage/v1/object/public/{bucket_name}/{file_path_in_bucket}"
                pdf_url = pdf_url.replace(":/", "://").replace("//", "/")

                st.write("⏳ Aguardando processamento do arquivo...")
                time.sleep(10)

                try:
                    request.urlopen(pdf_url)
                except Exception as e:
                    st.error(f"❌ Erro ao acessar o PDF: {str(e)}")
                    return

                # Insere no banco de dados
                response = supabase.table("preprovas").insert({"user_id": user_id, "pdf_url": pdf_url}).execute()

                if response.data:
                    preprova_id = response.data[0]["id"]
                    st.session_state["preprova_id"] = preprova_id
                    st.session_state["pdf_url"] = pdf_url

                    st.success("✅ PDF carregado com sucesso!")
                    st.info("👉 Acesse suas pré-provas no menu 'Pré-Prova'.")

                    # Gera questões
                    with st.spinner("Gerando questões..."):
                        success = generate_questions.generate_questions(preprova_id, pdf_url)
                        if success:
                            st.success("🎉 Questões geradas! Acesse 'Pré-Prova' no menu.")
                        else:
                            st.error("❌ Erro ao gerar questões.")

            except Exception as e:
                st.error(f"❌ Erro no upload: {str(e)}")
