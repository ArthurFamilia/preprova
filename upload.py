import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
import generate_questions  # Importa a função de geração de questões
import time
import re
import tempfile
from urllib import request

# Inicializa o cliente Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_pdf():
    st.title("Upload de Arquivo PDF")

    # 🔹 Obtém o usuário autenticado da sessão
    user_id = st.session_state.get("user_id")

    if not user_id:
        st.error("Usuário não autenticado. Faça login novamente.")
        return

    # 🔹 Debug: Verificar usuário logado
    st.write("Debug User:", user_id)

    uploaded_file = st.file_uploader("Selecione um arquivo PDF", type="pdf")
    
    if uploaded_file:
        if uploaded_file.size > 10 * 1024 * 1024:  # Limite de 10MB
            st.error("O arquivo excede o tamanho máximo permitido (10MB).")
            return

        with st.spinner("Carregando PDF..."):
            try:
                # 🔹 Remove espaços e caracteres especiais do nome do arquivo
                safe_file_name = re.sub(r'\s+', '_', uploaded_file.name)
                safe_file_name = re.sub(r'[^\w\-.]', '', safe_file_name)  # Remove caracteres especiais
                
                # 🔹 Adiciona timestamp para evitar duplicação
                timestamp = int(time.time())  
                file_path = f"pdfs/{timestamp}_{safe_file_name}"

                # 🔹 Salva o arquivo temporariamente antes do upload
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                    temp_file_path = temp_file.name

                # 🔹 Verifica se o arquivo já existe no Supabase Storage e remove
                existing_files = supabase.storage.from_("pdfs").list()
                file_names = [f["name"] for f in existing_files]

                for f in existing_files:
                    if safe_file_name in f["name"]:
                        supabase.storage.from_("pdfs").remove(f["name"])

                # 🔹 Faz o upload para o Supabase Storage
                with open(temp_file_path, "rb") as file_data:
                    storage_response = supabase.storage.from_("pdfs").upload(file_path, file_data)

                # 🔹 Confirma se o upload foi bem-sucedido
                if storage_response:
                    st.write("✅ Upload realizado com sucesso. Confirme no Supabase Storage.")
                else:
                    st.error("❌ Erro: O arquivo pode não ter sido enviado corretamente.")
                    return
                
                # 🔹 Obtém a URL pública do arquivo armazenado no Supabase
                pdf_url = supabase.storage.from_("pdfs").get_public_url(file_path)
                st.write(f"📄 PDF armazenado: [{safe_file_name}]({pdf_url})")

                # 🔹 Aguarda o Supabase processar o arquivo
                time.sleep(2)

                # 🔹 Testa se a URL está acessível
                try:
                    response = request.urlopen(pdf_url)
                    if response.status != 200:
                        raise Exception("Erro ao acessar o arquivo no Supabase Storage.")
                except Exception as e:
                    st.error(f"Erro ao acessar o PDF no Supabase: {str(e)}")
                    return

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
