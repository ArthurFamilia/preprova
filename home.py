import streamlit as st

def home_page():
    st.sidebar.title(f"Bem-vindo, {st.session_state['user_email']}")
    st.sidebar.header("Menu")
    
    st.title("Primeiro passo - Carregue seu arquivo para gerar a Pre Prova no menu esquerdo "Pre Prova"")
    st.title("Segundo passo  - Acesse o menu Pre prova para ver a prova gerada")
    st.title("Terceiro passo - Clique em Quiz para responder a pre prova")
   
