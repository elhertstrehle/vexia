import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Carregar os blocos v8
with open("vexia_blocos_estruturados_expandidos_v8_pt.json", "r", encoding="utf-8") as f:
    blocos = json.load(f)

# Extrair os textos para gerar embeddings
textos = [bloco["texto"] for bloco in blocos]

# Carregar o modelo de embedding
modelo = SentenceTransformer("all-MiniLM-L6-v2")

# Gerar embeddings
vetores = modelo.encode(textos, show_progress_bar=True)

# Criar índice FAISS
index = faiss.IndexFlatL2(vetores.shape[1])
index.add(np.array(vetores))

# Salvar o índice e os textos
faiss.write_index(index, "vexia_faiss_blocos_v8.index")

with open("vexia_frases_blocos_v8.json", "w", encoding="utf-8") as f:
    json.dump(textos, f, indent=2, ensure_ascii=False)

print("✅ Arquivos gerados com sucesso!")
