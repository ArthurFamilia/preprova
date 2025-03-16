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

    # 🔹 Se `user_id` for None, tenta buscar novamente no Supabase
    if not user_id:
        user_data = supabase.auth.get_user()
        if user_data and hasattr(user_data, "user") and user_data.user:
            user_id = user_data.user.id
            st.session_state["user_id"] = user_id

    if not user_id:
        st.error("Usuário não autenticado. Faça login novamente.")
        return

    # 🔹 Debug: Verificar usuário logado
    st.write("🔍 **DEBUG - Usuário Autenticado:**", user_id)

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

                # 🔹 Debug: Imprimir caminho do arquivo gerado
                st.write(f"📂 **DEBUG - Caminho do Arquivo no Supabase:** {file_path}")

                # 🔹 Salva o arquivo temporariamente antes do upload
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                    temp_file_path = temp_file.name

                # 🔹 Verifica se o bucket `pdfs` é público antes do upload
                bucket_info = supabase.storage.get_bucket("pdfs")
                st.write("📂 **DEBUG - Bucket Info:**", bucket_info)

                if not bucket_info["public"]:
                    st.error("❌ **Erro: O bucket 'pdfs' não está público!** Verifique no Supabase.")
                    return

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
                    st.write("✅ **DEBUG - Upload realizado com sucesso.** Confirme no Supabase Storage.")
                else:
                    st.error("❌ **DEBUG - O arquivo pode não ter sido enviado corretamente.**")
                    return
                
                # 🔹 Corrige a URL gerada para o Supabase
                pdf_url = f"{SUPABASE_URL}/storage/v1/object/public/{file_path}"
                st.write(f"📄 **DEBUG - PDF armazenado:** [{safe_file_name}]({pdf_url})")
                st.write(f"🔗 **DEBUG - URL Gerada:** {pdf_url}")

                # 🔹 Aguarda 10 segundos antes de acessar o arquivo
                st.write("⏳ **DEBUG - Aguardando 10 segundos para garantir que o Supabase processe o arquivo...**")
                time.sleep(10)

                # 🔹 Testa se a URL está acessível
                try:
                    response = request.urlopen(pdf_url)
                    if response.status == 200:
                        st.write("✅ **DEBUG - O arquivo está acessível no Supabase.**")
                    else:
                        raise Exception("Erro ao acessar o arquivo no Supabase Storage.")
                except Exception as e:
                    st.error(f"❌ **DEBUG - Erro ao acessar o PDF no Supabase:** {str(e)}")
                    return

                # 🔹 Revalida a sessão do usuário antes do INSERT
                session_info = supabase.auth.get_session()
                if session_info is None:
                    supabase.auth.refresh_session()
                    session_info = supabase.auth.get_session()
                    st.write(f"🔍 **DEBUG - Sessão Atualizada:** {session_info}")

                # 🔹 Criar uma pré-prova vinculada ao usuário logado
                st.write("📊 **DEBUG - Tentando inserir na tabela preprovas**")
                st.write(f"📊 **DEBUG - user_id:** {user_id}")
                st.write(f"📊 **DEBUG - pdf_url:** {pdf_url}")

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
                st.error(f"❌ **DEBUG - Erro no upload para o Supabase:** {str(e)}")
