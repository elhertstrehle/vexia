import streamlit as st
from sentence_transformers import SentenceTransformer, util
import json
import numpy as np
import os
import groq
from dotenv import load_dotenv

load_dotenv()
client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="VexIA Overlord", layout="wide")
st.title("🤖 VexIA - Mestre de RPG para Star Wars: Imperial Assault")

# Entrada do usuário
pergunta = st.text_input("Faça uma pergunta sobre o jogo:", "")

# Carregar blocos
with open("data/vexia_blocos_estruturados_expandidos_v8_pt.json", "r", encoding="utf-8") as f:
    blocos = json.load(f)

with open("data/vexia_blocos_ingles_base.json", "r", encoding="utf-8") as f:
    blocos_en = json.load(f)

with open("data/vexia_frases_ltp_boas.json", "r", encoding="utf-8") as f:
    frases_ltp = json.load(f)

# Carregar FAISS manualmente
import faiss
index = faiss.read_index("data/vexia_faiss_blocos_v8.index")

modelo = SentenceTransformer("all-MiniLM-L6-v2")

if pergunta:
    # 🔍 Roteador por palavra-chave
    pergunta_lower = pergunta.lower()
    tema_forcado = None

    if any(p in pergunta_lower for p in ["atacar", "ataque", "disparar", "golpe"]):
        tema_forcado = "acao_atacar"
    elif any(p in pergunta_lower for p in ["descansar", "curar", "recuperar", "tensão"]):
        tema_forcado = "acao_descansar"
    elif any(p in pergunta_lower for p in ["mover", "movimento", "deslocar"]):
        tema_forcado = "movimento"
    elif any(p in pergunta_lower for p in ["linha de visão", "enxergar", "ver", "alvo visível"]):
        tema_forcado = "linha_visao"
    elif any(p in pergunta_lower for p in ["precisão", "distância", "alcance"]):
        tema_forcado = "precisao"

    if tema_forcado:
        bloco = next((b for b in blocos if b["tema"] == tema_forcado), {})
        if bloco:
            tema = bloco["tema"]
            resumo = bloco.get("descricao", "")
            tecnico = blocos_en.get(tema, "")
        else:
            tema = "tema_indefinido"
            bloco = {
                "tema": "desconhecido",
                "descricao": "A palavra-chave foi detectada, mas o bloco correspondente não foi encontrado.",
                "excecoes": "",
                "exemplos": "",
                "origem": ""
            }
            resumo = bloco["descricao"]
            tecnico = ""
    else:
        temas_texto = [b.get("descricao", "") for b in blocos]
        temas_embed = modelo.encode(temas_texto, convert_to_tensor=True)
        pergunta_embed = modelo.encode(pergunta, convert_to_tensor=True)
        sim_scores = util.cos_sim(pergunta_embed, temas_embed)[0]
        idx_tema = int(np.argmax(sim_scores))
        confianca = float(sim_scores[idx_tema])

        if confianca < 0.35:
            tema = "tema_indefinido"
            bloco = {
                "tema": "desconhecido",
                "descricao": "A pergunta não pôde ser associada claramente a um tema específico.",
                "excecoes": "",
                "exemplos": "",
                "origem": ""
            }
            resumo = bloco["descricao"]
            tecnico = ""
        else:
            bloco = blocos[idx_tema]
            tema = bloco["tema"]
            resumo = bloco.get("descricao", "")
            tecnico = blocos_en.get(tema, "")


    # Mostrar informações do tema identificado
    st.markdown(f"### 🧠 Tema identificado: **{tema}**")
    st.markdown(f"📘 **Descrição:** {resumo}")
    if bloco.get("excecoes"):
        st.markdown("**⚠️ Exceções:**")
        st.code(bloco["excecoes"])
    if bloco.get("exemplos"):
        st.markdown("**📌 Exemplos:**")
        st.code(bloco["exemplos"])
    if bloco.get("origem"):
        st.markdown(f"**📎 Origem da Regra:** {bloco['origem']}")
    # Buscar frases do manual por FAISS
    pergunta_vector = modelo.encode([pergunta])
    top_k = 4
    D, I = index.search(np.array(pergunta_vector), top_k)
    trechos = [frases_ltp.get(str(i), "") for i in I[0] if str(i) in frases_ltp]

    st.markdown("📚 **Trechos adicionais do manual:**")
    for trecho in trechos:
        st.markdown(f"- {trecho}")


    # Montar prompt final para Groq
    lista_trechos = "\n".join(f"- {t}" for t in trechos)

    prompt = f"""
Você é VexIA, uma IA mestre de RPG especializada em Star Wars: Imperial Assault.
Responda em português natural com base nos manuais oficiais do jogo.
Use o bloco temático como base principal e os trechos adicionais apenas como reforço, sem inventar regras.

❓ Pergunta: {pergunta}

📘 Bloco principal ({tema}): 
{resumo}

📘 Technical reference (EN): 
{tecnico}

📚 Trechos adicionais do manual:
{lista_trechos}

🎯 Responda de forma clara, didática, fiel às regras e sem sair do tema.
    """.strip()
    st.markdown("🔧 Prompt completo enviado à IA")
    st.code(prompt)

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    st.markdown("💬 **Resposta da VexIA:**")
    st.markdown(response.choices[0].message.content.strip())
