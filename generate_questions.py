import openai
import fitz  # PyMuPDF para extrair texto do PDF
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, OPENAI_KEY
import streamlit as st

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
client = openai.OpenAI(api_key=OPENAI_KEY)  # Nova sintaxe para OpenAI

def generate_questions(preprova_id, pdf_url):
    """Gera questões com base no texto do PDF usando OpenAI."""
    st.write(f"📂 DEBUG - Extraindo texto do PDF: {pdf_url}")

    pdf_text = extract_text_from_pdf(pdf_url)
    if not pdf_text:
        st.error("❌ DEBUG - Nenhum texto extraído do PDF. Abortando geração de questões.")
        return False

    prompt = f"Crie 5 perguntas no formato flashcards com base neste texto:\n{pdf_text[:2000]}"

    try:
        response = client.chat.completions.create(  # ✅ Atualizado para a API openai>=1.0.0
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um criador de flashcards para estudo médico."},
                {"role": "user", "content": prompt}
            ]
        )

        if response and response.choices:
            questions = [choice.message.content for choice in response.choices]

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
