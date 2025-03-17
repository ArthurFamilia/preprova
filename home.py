import streamlit as st

def home_page():
    st.title("📌 Guia Rápido para sua Pré-Prova")

    st.markdown("""
    1️⃣ **Primeiro Passo** - 📤 **Carregue seu arquivo** no menu **"Upload PDF"** na barra lateral.
    
    2️⃣ **Segundo Passo** - 📑 **Acesse "Pré-Prova"** para visualizar a prova gerada.
    
    3️⃣ **Terceiro Passo** - 📝 **Clique em "Quiz"** para responder às questões da pré-prova.
    """)

    st.info("📢 **Dica:** Certifique-se de que seu PDF contém informações relevantes para gerar boas questões!")
    st.info("📢 **Dica:** Quebre o arquivo em menos páginas para concentrar o foco em um assunto específico. Use o [iLovePDF](https://www.ilovepdf.com/split_pdf#split,range) para dividir o PDF facilmente.")


if __name__ == "__main__":
    home_page()
