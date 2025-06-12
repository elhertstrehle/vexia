# Projeto VexIA

## Visão Geral

VexIA é uma Inteligência Artificial especializada em jogos de tabuleiro e RPGs, com foco inicial no jogo **Star Wars: Imperial Assault**. Seu objetivo é simular um mestre de jogo (Overlord) capaz de interpretar as regras, responder perguntas em linguagem natural e atuar como narrador e controlador de elementos do jogo.

O projeto prioriza o uso de ferramentas **100% gratuitas** e de **código aberto**, mantendo foco em performance, expansibilidade e compatibilidade com futuras monetizações.

---

## Estrutura Atual do Projeto

```
vexia/
├── .env                        # Variáveis de ambiente (com chave da API Groq)
├── .env.example                # Exemplo de .env para novos ambientes
├── .gitignore                 # Ignora .env, arquivos temporários, etc.
├── README.md                  # Documento principal do projeto
├── requirements.txt           # Dependências do projeto Python
├── VexIA.bat                  # Atalho para execução local no Windows
│
├── app/
│   └── vexia_groq_v12.py      # Script principal da IA com interface Streamlit
│
├── data/                      # Base de conhecimento e index semântico
│   ├── gerar_index_v8.py
│   ├── vexia_blocos_estruturados_expandidos_v8_pt.json
│   ├── vexia_blocos_ingles_base.json
│   ├── vexia_faiss_blocos_v8.index
│   ├── vexia_frases_blocos_v8.json
│   ├── vexia_frases_ltp_boas.json
│   └── vexia_frases_ltp_corrigidas.json
│
├── docs/                      # Documentação adicional
│   └── README.md
│
└── scripts/                   # Scripts auxiliares (reconstrução, testes)
    └── reconstruir_index.py
```

---

## Componentes e Etapas Concluídas

### ✅ Regras e Fontes Oficiais

* Upload dos manuais oficiais em PDF:

  * Learn to Play (inglês)
  * Rules Reference (inglês)
  * Traduções em português (base textual para IA)

### ✅ Blocos Temáticos Expandidos

* Reestruturação dos blocos de regras em português natural
* Divisão por tema, com campos:

  * `tema`, `descricao`, `excecoes`, `exemplos`, `origem`, `fonte_paginas`, `texto`
* Versão atual: `vexia_blocos_estruturados_expandidos_v8_pt.json`

### ✅ Base Vetorial

* Gerada com `sentence-transformers` e `faiss-cpu`
* Frases extraídas e ajustadas com:

  * `vexia_frases_ltp_corrigidas.json`
  * `vexia_frases_blocos_v8.json`
* Index final: `vexia_faiss_blocos_v8.index`

### ✅ Interface VexIA

* Interface Streamlit responsiva e funcional
* Prompt estruturado com resposta em linguagem natural
* Detecção de tema, uso do bloco principal e reforço com semântica
* Versão atual: `vexia_groq_v12.py`

---

## Desafios Superados

* Corrupção de arquivos `.index` via upload
* Compatibilidade entre versões do arquivo `.env`
* Erros de indentacão e `KeyError` em execução
* Geração local e organização de pastas para execução limpa

---

## Objetivos Atuais

*

---

## Planos Futuros

* Integração com voz e OCR (ex: leitura de fotos do tabuleiro)
* Modo narrador com leitura em voz alta e ambientação sonora
* Compatibilidade com outros jogos (Massive Darkness, Gloomhaven, etc.)
* Portal público com API para uso em aplicativos e mesas virtuais

---

## Execução Local

### Requisitos

```bash
pip install -r requirements.txt
```

### Execução

```bash
streamlit run app/vexia_groq_v12.py
```

---

## Licença e Uso

Este é um projeto experimental com fins educacionais e recreativos. O uso de material traduzido segue a diretriz de "fair use" para uso não comercial.

---

## Contribuições

Sugestões, relatórios de erros ou contribuições com regras e blocos são bem-vindas via Pull Request ou Issues no GitHub.

---

**Que a Força esteja com VexIA!** 🤖💡
