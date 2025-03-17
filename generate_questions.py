import openai
import fitz  # PyMuPDF para extrair texto do PDF
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, OPENAI_KEY
import streamlit as st
import time
import re

# Inicializa os clientes
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
client = openai.OpenAI(api_key=OPENAI_KEY)

def extract_text_from_pdf(pdf_url):
    """Baixa o PDF do Supabase e extrai o texto."""
    st.write(f"📂 DEBUG - Extraindo texto do PDF: {pdf_url}")
    pdf_url = re.sub(r'(?<!:)//+', '/', pdf_url)
    file_path_in_bucket = pdf_url.replace(f"{SUPABASE_URL}/storage/v1/object/public/pdfs/", "")
    
    st.write("⏳ DEBUG - Aguardando 10 segundos antes do download...")
    time.sleep(10)

    try:
        response = supabase.storage.from_("pdfs").download(file_path_in_bucket)
        if not response:
            st.error(f"❌ DEBUG - Erro ao baixar o PDF do Supabase: {file_path_in_bucket} não encontrado.")
            return None

        with fitz.open(stream=response, filetype="pdf") as doc:
            text = "\n".join([page.get_text("text") for page in doc])

        return text
    except Exception as e:
        st.error(f"❌ DEBUG - Erro ao extrair texto do PDF: {str(e)}")
        return None

def generate_questions(preprova_id, pdf_url):
    """Gera questões e salva no banco"""
    st.write("📂 DEBUG - Iniciando geração de questões.")
    pdf_text = extract_text_from_pdf(pdf_url)
    if not pdf_text:
        st.error("❌ DEBUG - Nenhum texto extraído do PDF. Abortando geração de questões.")
        return False
    
    prompt = f"""
    Gere 5 questões de múltipla escolha com 4 alternativas cada uma.
    Formato:
    Pergunta: (texto da pergunta)
    Opções:
    A) (opção 1)
    B) (opção 2)
    C) (opção 3)
    D) (opção 4)
    Resposta correta: (letra correta)
    
    Baseie-se no seguinte conteúdo:
    {pdf_text[:2000]}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um criador de questões para estudo médico."},
                {"role": "user", "content": prompt}
            ]
        )

        questions = response.choices[0].message.content.split("\n\n")

        for question_block in questions:
            lines = question_block.split("\n")
            if len(lines) < 6:
                continue  # Ignorar blocos mal formados

            pergunta = lines[0].replace("Pergunta: ", "")
            opcao_a = lines[1].replace("A) ", "")
            opcao_b = lines[2].replace("B) ", "")
            opcao_c = lines[3].replace("C) ", "")
            opcao_d = lines[4].replace("D) ", "")
            resposta_correta = lines[5].replace("Resposta correta: ", "")

            supabase.table("questoes").insert({
                "preprova_id": preprova_id,
                "pergunta": pergunta,
                "opcao_a": opcao_a,
                "opcao_b": opcao_b,
                "opcao_c": opcao_c,
                "opcao_d": opcao_d,
                "resposta_correta": resposta_correta
            }).execute()

        st.success("✅ DEBUG - Questões geradas e armazenadas com sucesso.")
        return True
    except Exception as e:
        st.error(f"❌ DEBUG - Erro ao gerar perguntas com OpenAI: {str(e)}")
        return False
