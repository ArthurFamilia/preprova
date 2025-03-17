import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def quiz_page():
    st.title("Quiz da Pré-Prova")

    preprova_id = st.session_state.get("preprova_id")
    if not preprova_id:
        st.error("Nenhuma pré-prova selecionada. Volte ao menu e escolha uma.")
        return

    response = supabase.table("questoes").select("*").eq("preprova_id", preprova_id).execute()

    if not response.data:
        st.warning("Nenhuma questão encontrada para esta pré-prova.")
        return

    st.write("📖 **Responda as perguntas abaixo:**")

    respostas_usuario = {}
    respostas_corretas = {}
    total_questoes = len(response.data)

    # Criando um formulário para capturar todas as respostas de uma vez
    with st.form("quiz_form"):
        for questao in response.data:
            st.subheader(f"❓ {questao['pergunta']}")

            # Garante que todas as opções existem, evitando erro KeyError
            opcoes = [
                questao.get("opcao_a", "A) Alternativa não fornecida"),
                questao.get("opcao_b", "B) Alternativa não fornecida"),
                questao.get("opcao_c", "C) Alternativa não fornecida"),
                questao.get("opcao_d", "D) Alternativa não fornecida")
            ]

            resposta = st.radio(
                "Escolha a resposta:",
                options=opcoes,
                key=f"resp_{questao['id']}"
            )
            respostas_usuario[questao["id"]] = resposta
            respostas_corretas[questao["id"]] = questao.get("resposta_correta", "").strip()

        # Garante que o botão de envio está presente no formulário
        enviar = st.form_submit_button("Enviar Respostas", type="primary")

    if enviar:
        st.write("📊 **Resultado:**")

        acertos = 0
        for questao in response.data:
            resposta_usuario = respostas_usuario.get(questao["id"], "").strip()
            resposta_correta = respostas_corretas.get(questao["id"], "").strip()

            if resposta_usuario == resposta_correta:
                acertos += 1
                st.success(f"✅ {questao['pergunta']} - Correto!")
            else:
                st.error(f"❌ {questao['pergunta']} - Resposta correta: {resposta_correta}")

        nota = (acertos / total_questoes) * 10
        st.markdown(f"🎯 **Sua nota: {nota:.2f}/10**")

if __name__ == "__main__":
    quiz_page()
