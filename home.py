import streamlit as st

def home_page():
    st.sidebar.title(f"👋 Bem-vindo, {st.session_state['user_email']}")
    
    # 📌 Adicionando um menu lateral com ícones
    st.sidebar.header("📜 Menu de Navegação")
    st.sidebar.markdown("🏠 **Home**")
    st.sidebar.markdown("📤 **Upload PDF**")
    st.sidebar.markdown("📑 **Pré-Prova**")
    st.sidebar.markdown("📝 **Quiz**")
    st.sidebar.markdown("🚪 **Sair**")

    # 🎯 Passos com ícones e formatação bonita
    st.title("📌 Guia Rápido para sua Pré-Prova")

    st.markdown("""
    1️⃣ **Primeiro Passo** - 📤 **Carregue seu arquivo** no menu **"Upload PDF"** na barra lateral.
    
    2️⃣ **Segundo Passo** - 📑 **Acesse "Pré-Prova"** para visualizar a prova gerada.
    
    3️⃣ **Terceiro Passo** - 📝 **Clique em "Quiz"** para responder às questões da pré-prova.
    """)

    st.info("📢 **Dica:** Certifique-se de que seu PDF contém informações relevantes para gerar boas questões!")

if __name__ == "__main__":
    home_page()
