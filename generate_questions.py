import openai
import fitz  # PyMuPDF para extrair texto do PDF
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, OPENAI_KEY
import streamlit as st

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
openai.api_key = OPENAI_KEY

def extract_text_from_pdf(pdf_url):
    """Baixa o PDF do Supabase e extrai o texto."""
    response = supabase.storage.from_("pdfs").download(pdf_url)
    if response is None:
        return None

    with fitz.open(stream=response, filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
    return text

def generate_questions(preprova_id, pdf_url):
    """Gera questões com base no texto do PDF usando OpenAI."""
    st.write("cp 0" + pdf_url)
    
    # pdf_url = pdf_url.replace('/pdfs/pdfs/', '/pdfs/')
    st.write("nova _url"  + pdf_url)
    pdf_url = extract_text_from_pdf(pdf_url)
    if not text:
        return None
        
    st.write("cp 1")
    prompt = f"Crie 5 perguntas no formato flashcards com base neste texto:\n{text[:2000]}"  # Limitamos a 2000 caracteres

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Você é um criador de flashcards para estudo médico."},
                  {"role": "user", "content": prompt}]
    )
    st.write("cp 2")
    if response:
        questions = [msg["content"] for msg in response["choices"]]
        
        # Insere as perguntas na tabela `questoes`
        for pergunta in questions:
            supabase.table("questoes").insert({"preprova_id": preprova_id, "pergunta": pergunta}).execute()

        return True
    else:
        st.write("cp 3")
        return False
