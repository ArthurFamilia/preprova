import streamlit as st

def preprova_page():
    st.title("Pré-Prova")

    # Verifica se os dados necessários estão disponíveis
    if "preprova_id" not in st.session_state or "pdf_url" not in st.session_state:
        st.error("Erro: Nenhuma pré-prova encontrada. Faça o upload de um PDF primeiro.")
        return

    preprova_id = st.session_state["preprova_id"]
    pdf_url = st.session_state["pdf_url"]

    st.write(f"📂 ID da Pré-Prova: {preprova_id}")
    st.write(f"📄 PDF: [{pdf_url}]({pdf_url})")

    # Aqui pode adicionar a lógica para exibir perguntas ou permitir download

if __name__ == "__main__":
    preprova_page()

