import streamlit as st

def login_page(supabase):
    st.title("Pre Prova Medicina")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("logo.jpg", width=341)
    with col2:
        st.markdown("<h3>Sua Inteligência, nossa IA, rumo ao seu jaleco branco.</h3>", unsafe_allow_html=True)
    
    login_option = st.radio("Escolha uma opção:", ("Login", "Cadastro"))
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")
    
    if login_option == "Login":
        if st.button("Entrar"):
            try:
                response = supabase.auth.sign_in_with_password({"email": email, "password": password})
                if hasattr(response, "user") and response.user:
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = email
                    st.rerun()
                else:
                    st.error("Email ou senha incorretos.")
            except Exception as e:
                if "Invalid login credentials" in str(e):
                    st.error("Usuário não cadastrado ou senha incorreta. Tente novamente ou cadastre-se.")
                else:
                    st.error(f"Erro no login: {str(e)}")
    
    else:  # Cadastro
        if st.button("Cadastrar"):
            if len(password) < 6:
                st.error("A senha deve ter pelo menos 6 caracteres.")
            else:
                try:
                    response = supabase.auth.sign_up({"email": email, "password": password})
                    if hasattr(response, "user") and response.user:
                        st.success("Cadastro realizado com sucesso! Faça login.")
                    else:
                        st.error("Erro ao cadastrar usuário. Tente outro email.")
                except Exception as e:
                    st.error(f"Erro no cadastro: {str(e)}")
