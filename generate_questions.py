import openai
import fitz  # PyMuPDF para extrair texto do PDF
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, OPENAI_KEY
import streamlit as st

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
client = openai.OpenAI(api_key=OPENAI_KEY)  # Nova sintaxe para a API

def extract_text_from_pdf(pdf_url):
    """Baixa o PDF do Supabase e extrai o texto."""
    st.write(f"📂 DEBUG - Tentando baixar o arquivo com caminho: {pdf_url}")

    try:
        response = supabase.storage.from_("pdfs").download(pdf_url)
        if not response:
            st.error(f"❌ DEBUG - O arquivo '{pdf_url}' NÃO FOI ENCONTRADO no bucket!")
            return None

        with fitz.open(stream=response, filetype="pdf") as doc:
            text = "\n".join([page.get_text("text") for page in doc])

        st.write("📂 DEBUG - Texto extraído com sucesso.")
        return text
    except Exception as e:
        st.error(f"❌ DEBUG - Erro ao extrair texto do PDF: {str(e)}")
        return None

def generate_questions(preprova_id, pdf_url):
    """Gera questões com base no texto do PDF usando OpenAI GPT-4o mini."""
    st.write(f"📂 DEBUG - Extraindo texto do PDF: {pdf_url}")

    pdf_text = extract_text_from_pdf(pdf_url)
    if not pdf_text:
        st.error("❌ DEBUG - Nenhum texto extraído do PDF. Abortando geração de questões.")
        return False

    st.write("📂 DEBUG - Texto extraído, enviando para OpenAI.")

    prompt = f"Crie 5 perguntas no formato flashcards com base neste texto:\n{pdf_text[:2000]}"

    try:
        response = client.chat.completions.create(  # ✅ Nova sintaxe
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": "Você é um criador de flashcards para estudo médico."},
                {"role": "user", "content": prompt}
            ]
        )

        # ✅ Obtendo resposta da nova API corretamente
        questions = [choice.message.content for choice in response.choices]

        # Insere as perguntas na tabela `questoes`
        for pergunta in questions:
            supabase.table("questoes").insert({"preprova_id": preprova_id, "pergunta": pergunta}).execute()

        st.success("🎉 Questões geradas com sucesso!")
        return True
    except Exception as e:
        st.error(f"❌ DEBUG - Erro ao gerar perguntas com OpenAI: {str(e)}")
        return False
