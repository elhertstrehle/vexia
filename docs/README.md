# VexIA

VexIA é uma IA mestre de RPGs e BoardGames, com foco inicial em *Star Wars: Imperial Assault*. Ela responde a perguntas dos jogadores com base nos manuais oficiais, combinando blocos temáticos, busca vetorial (FAISS) e geração via LLM.

## Como rodar

1. Instale as dependências:

```
pip install streamlit sentence-transformers faiss-cpu groq
```

2. Adicione sua chave Groq em `~/.streamlit/secrets.toml`:

```
groq_api_key = "sua_chave_aqui"
```

3. Reconstrua o índice FAISS:

```
python reconstruir_index.py
```

4. Execute a VexIA:

```
streamlit run vexia_groq_v12.py
```
