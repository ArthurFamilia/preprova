import streamlit as st
from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def login_page():
    st.title("Pre Prova Medicina")

    login_option = st.radio("Escolha uma opção:", ("Login", "Cadastro"))
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")

    if login_option == "Login":
        if st.button("Entrar"):
            try:
                # Faz login
                auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})

                # Se o login foi bem-sucedido, obtém o usuário autenticado
                if hasattr(auth_response, "user") and auth_response.user:
                    user_data = supabase.auth.get_user()
                    
                    # Verifica se o e-mail foi confirmado
                    if not user_data.user.email_confirmed_at:
                        st.error("Seu e-mail ainda não foi confirmado. Verifique sua caixa de entrada.")
                        return

                    # Login autorizado
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
                return
            
            try:
                # 🔹 Verifica se o email já existe antes de cadastrar
                existing_user = supabase.table("auth.users").select("id").eq("email", email).execute()
                
                if existing_user.data:
                    st.error("Este e-mail já está cadastrado. Tente outro ou faça login.")
                    return

                # Criar usuário no Supabase
                signup_response = supabase.auth.sign_up({"email": email, "password": password})
                
                if hasattr(signup_response, "user") and signup_response.user:
                    st.success("Cadastro realizado com sucesso! Confirme seu e-mail antes de fazer login.")
                else:
                    st.error("Erro ao cadastrar usuário. Tente outro email.")

            except Exception as e:
                st.error(f"Erro no cadastro: {str(e)}")
