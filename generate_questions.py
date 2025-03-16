import openai
import fitz  # PyMuPDF para extrair texto do PDF
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, OPENAI_KEY
import streamlit as st
import time
import re

# Inicializa os clientes
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
openai.api_key = OPENAI_KEY

def extract_text_from_pdf(pdf_url):
    """Baixa o PDF do Supabase e extrai o texto."""

    st.write(f"📂 DEBUG - Extraindo texto do PDF: {pdf_url}")

    # 🔹 Verifica se a URL pública tem barras duplas e remove
    pdf_url = re.sub(r'(?<!:)//+', '/', pdf_url)

    # 🔹 Obtém apenas o nome do arquivo do Supabase Storage
    file_path_in_bucket = pdf_url.replace(f"{SUPABASE_URL}/storage/v1/object/public/pdfs/", "")

    st.write(f"📂 DEBUG - Caminho absoluto do arquivo salvo na tabela: {file_path_in_bucket}")

    # 🔹 Aguarda 10 segundos para garantir que o Supabase processe o upload
    st.write("⏳ DEBUG - Aguardando 10 segundos antes do download...")
    time.sleep(10)

    # 🔹 Lista arquivos disponíveis no bucket para depuração
    try:
        existing_files = supabase.storage.from_("pdfs").list()
        existing_file_names = [file["name"] for file in existing_files]

        st.write(f"📂 DEBUG - Arquivos disponíveis no bucket: {existing_file_names}")

        # 🔹 Verifica se o arquivo realmente existe no bucket antes de tentar baixar
        if file_path_in_bucket not in existing_file_names:
            st.error(f"❌ DEBUG - O arquivo '{file_path_in_bucket}' NÃO FOI ENCONTRADO no bucket!")
            return None
    except Exception as e:
        st.error(f"❌ DEBUG - Erro ao listar arquivos do Supabase: {str(e)}")
        return None

    # 🔹 Tenta baixar o arquivo usando apenas o nome correto do arquivo
    try:
        st.write(f"📂 DEBUG - Tentando baixar o arquivo com caminho correto: {file_path_in_bucket}")

        response = supabase.storage.from_("pdfs").download(file_path_in_bucket)

        if not response:
            st.error(f"❌ DEBUG - Erro ao baixar o PDF do Supabase: {file_path_in_bucket} não encontrado.")
            return None

        st.write(f"✅ DEBUG - Arquivo baixado com sucesso.")

        # 🔹 Lendo o conteúdo do PDF
        with fitz.open(stream=response, filetype="pdf") as doc:
            text = "\n".join([page.get_text("text") for page in doc])
        
        st.write("✅ DEBUG - Texto extraído com sucesso.")
        return text
    except Exception as e:
        st.error(f"❌ DEBUG - Erro ao extrair texto do PDF: {str(e)}")
        return None

def generate_questions(preprova_id, pdf_url):
    """Gera questões com base no texto do PDF usando OpenAI."""
    
    st.write("📂 DEBUG - Iniciando geração de questões.")

    # 🔹 Extração de texto corrigida
    pdf_text = extract_text_from_pdf(pdf_url)

    if not pdf_text:
        st.error("❌ DEBUG - Nenhum texto extraído do PDF. Abortando geração de questões.")
        return False
    
    st.write("📂 DEBUG - Criando prompt para OpenAI.")

    # 🔹 Limita a 2000 caracteres para evitar estouro de contexto
    prompt = f"Crie 5 perguntas no formato flashcards com base neste texto:\n{pdf_text[:2000]}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Você é um criador de flashcards para estudo médico."},
                      {"role": "user", "content": prompt}]
        )

        if response and "choices" in response:
            questions = [choice["message"]["content"] for choice in response["choices"]]

            # 🔹 Insere as perguntas na tabela `questoes`
            for pergunta in questions:
                supabase.table("questoes").insert({"preprova_id": preprova_id, "pergunta": pergunta}).execute()

            st.success("✅ DEBUG - Questões geradas e armazenadas com sucesso.")
            return True
        else:
            st.error("❌ DEBUG - Erro na resposta da OpenAI.")
            return False
    except Exception as e:
        st.error(f"❌ DEBUG - Erro ao gerar perguntas com OpenAI: {str(e)}")
        return False
