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

    st.write("📝 Responda as perguntas abaixo:")
    respostas_usuario = {}

    for questao in response.data:
        opcoes = [questao.get("opcao_a", "A"), questao.get("opcao_b", "B"), questao.get("opcao_c", "C"), questao.get("opcao_d", "D")]
        resposta = st.radio(f"❓ {questao['pergunta']}", opcoes, key=f"resp_{questao['id']}")
        respostas_usuario[questao["id"]] = resposta

    if st.button("Enviar Respostas"):
        st.write("📊 Resultado:")
        
        respostas_certas = 0
        total_questoes = len(response.data)

        for questao in response.data:
            resposta_correta = questao.get("resposta_correta", "").strip()
            resposta_usuario = respostas_usuario.get(questao["id"], "").strip()

            if resposta_usuario == resposta_correta:
                respostas_certas += 1
                st.success(f"✅ {questao['pergunta']} - Correto!")
            else:
                st.error(f"❌ {questao['pergunta']} - Resposta correta: {resposta_correta}")

        nota = (respostas_certas / total_questoes) * 10
        st.write(f"🎯 Sua nota: **{nota:.2f}/10**")

if __name__ == "__main__":
    quiz_page()
