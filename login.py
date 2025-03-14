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
                # Verifica se o e-mail foi confirmado na auth.users
                response = supabase.table("auth.users").select("confirmed_at").eq("email", email).execute()

                if not response.data or response.data[0].get("confirmed_at") is None:
                    st.error("Seu e-mail ainda não foi confirmado. Verifique sua caixa de entrada.")
                    return

                # Se estiver confirmado, tenta fazer login
                auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})

                if hasattr(auth_response, "user") and auth_response.user:
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = email
                    st.experimental_rerun()
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
                    signup_response = supabase.auth.sign_up({"email": email, "password": password})
                    if hasattr(signup_response, "user") and signup_response.user:
                        st.success("Cadastro realizado com sucesso! Confirme seu e-mail antes de fazer login.")
                    else:
                        st.error("Erro ao cadastrar usuário. Tente outro email.")
                except Exception as e:
                    st.error(f"Erro no cadastro: {str(e)}")
