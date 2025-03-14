import streamlit as st

def home_page():
    st.sidebar.title(f"Bem-vindo, {st.session_state['user_email']}")
    st.sidebar.header("Menu")
    
    st.title("Carregue seu arquivo para gerar a Pre Prova")
    uploaded_file = st.file_uploader("Escolha um arquivo (PDF ou imagem, até 10MB)", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=False)
    
    if uploaded_file:
        st.success("Arquivo carregado com sucesso!")
        if st.button("Criar Pre Prova"):
            st.write("Gerando perguntas... (Integração com IA aqui)")
            # Aqui entra a lógica para processar o arquivo e criar os flashcards
