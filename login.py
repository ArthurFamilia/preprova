import streamlit as st
from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def login_page():
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
                auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})

                if hasattr(auth_response, "user") and auth_response.user:
                    user_data = supabase.auth.get_user()
                    
                    # 🔹 Exibe informações do usuário para debug
                    st.write("Debug User:", user_data)

                    # 🔹 Verifica se o e-mail foi confirmado
                    if not user_data.user.email_confirmed_at:
                        st.error("Seu e-mail ainda não foi confirmado. Verifique sua caixa de entrada.")
                        return

                    # 🔹 Salva os dados do usuário na sessão
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = email
                    st.session_state["user_id"] = user_data.user.id  # Salva o ID do usuário

                    st.success("✅ Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Email ou senha incorretos.")
            except Exception as e:
                if "Invalid login credentials" in str(e):
                    st.error("Usuário não cadastrado ou senha incorreta. Tente novamente ou cadastre-se.")
                else:
                    st.error(f"Erro no login: {str(e)}")

    else:  # Cadastro
        if st.button("Cadastrar"):
            if len(password) < 6:
                st.error("A senha deve ter pelo menos 6 caracteres.")
                return
            
            try:
                # 🔹 Verifica se o e-mail já está cadastrado
                existing_user = supabase.auth.sign_in_with_password({"email": email, "password": password})
                
                if hasattr(existing_user, "user") and existing_user.user:
                    st.error("Este e-mail já está cadastrado. Tente outro ou faça login.")
                    return

            except Exception as e:
                if "Invalid login credentials" in str(e):
                    pass  # Usuário não existe, então podemos cadastrar

            # 🔹 Criar usuário no Supabase
            try:
                signup_response = supabase.auth.sign_up({"email": email, "password": password})
                
                if hasattr(signup_response, "user") and signup_response.user:
                    st.success("✅ Cadastro realizado com sucesso! Confirme seu e-mail antes de fazer login.")
                else:
                    st.error("❌ Erro ao cadastrar usuário. Tente outro email.")

            except Exception as e:
                if "User already registered" in str(e):
                    st.error("Este e-mail já está cadastrado. Tente outro ou faça login.")
                else:
                    st.error(f"Erro no cadastro: {str(e)}")
