def generate_questions(preprova_id, pdf_url):
    """Gera 10 questões e salva no banco"""
    st.write("📂 DEBUG - Iniciando geração de questões.")
    pdf_text = extract_text_from_pdf(pdf_url)
    if not pdf_text:
        st.error("❌ DEBUG - Nenhum texto extraído do PDF. Abortando geração de questões.")
        return False
    
    prompt = f"""
    Gere 10 questões de múltipla escolha com 4 alternativas cada uma.
    **Formato de saída (respeite exatamente esse padrão):**
    
    Pergunta: (texto da pergunta)
    A) (alternativa A)
    B) (alternativa B)
    C) (alternativa C)
    D) (alternativa D)
    Resposta correta: (Letra da alternativa correta: A, B, C ou D)
    
    Baseie-se no seguinte conteúdo:
    {pdf_text[:3000]}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um criador de questões para estudo médico."},
                {"role": "user", "content": prompt}
            ]
        )

        questions = response.choices[0].message.content.split("\n\n")

        for question_block in questions:
            lines = question_block.split("\n")
            if len(lines) < 6:
                continue  

            pergunta = lines[0].replace("Pergunta: ", "").strip()
            opcao_a = lines[1].replace("A) ", "").strip()
            opcao_b = lines[2].replace("B) ", "").strip()
            opcao_c = lines[3].replace("C) ", "").strip()
            opcao_d = lines[4].replace("D) ", "").strip()
            resposta_correta = lines[5].replace("Resposta correta: ", "").strip().upper()

            if resposta_correta not in ["A", "B", "C", "D"]:
                st.error(f"⚠️ Erro: Resposta correta inválida para pergunta '{pergunta}'")
                continue  

            supabase.table("questoes").insert({
                "preprova_id": preprova_id,
                "pergunta": pergunta,
                "opcao_a": opcao_a,
                "opcao_b": opcao_b,
                "opcao_c": opcao_c,
                "opcao_d": opcao_d,
                "resposta_correta": resposta_correta
            }).execute()

        st.success("✅ DEBUG - 10 Questões geradas e armazenadas com sucesso.")
        return True
    except Exception as e:
        st.error(f"❌ DEBUG - Erro ao gerar perguntas com OpenAI: {str(e)}")
        return False
