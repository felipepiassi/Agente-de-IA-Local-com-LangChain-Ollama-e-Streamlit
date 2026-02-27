# Agente-de-IA-Local-com-LangChain-Ollama-e-Streamlit
Agente de Inteligência Artificial local utilizando Python e Ollama

# 🤖 Agente de IA Local com LangChain e Ollama

Este projeto é um Agente de Inteligência Artificial executado localmente, desenvolvido em Python, utilizando LangChain, Ollama e Streamlit.

O agente é capaz de:

- Conversar com o usuário
- Pesquisar informações na internet
- Analisar arquivos CSV
- Utilizar um modelo de linguagem local (LLM)
- Manter contexto da conversa

---

## 🚀 Tecnologias utilizadas

- Python
- LangChain
- Ollama
- Streamlit
- Pandas
- DuckDuckGo Search
- LangGraph

---

## 🧠 Arquitetura

O agente utiliza o padrão ReAct (Reasoning + Acting), permitindo:

- Raciocinar
- Decidir quando usar ferramentas
- Buscar informações externas
- Responder com contexto

---

## 📊 Funcionalidade de análise de CSV

O usuário pode carregar um arquivo CSV e o agente pode:

- Ler os dados
- Analisar estatísticas
- Responder perguntas sobre o arquivo

---

## 🔐 Execução local

Este projeto executa completamente local, sem necessidade de APIs pagas.

📁 1. Estrutura ideal do projeto

agente-ia-local/
│
└── venv/  ----( para trabalhar com ambiente virtual, navegue ate a pasta do projeto para executar o ambiente virtual)
├── agente_pc.py
├── requirements.txt
├── README.md
├── .gitignore
└── assets/
    └── preview.png   (opcional - imagem do projeto)

📄 2. requirements.txt

streamlit
pandas
langchain
langchain-core
langchain-community
langchain-ollama
langgraph
duckduckgo-search
ollama

 Local URL: http://localhost:8501    ---- streamlit web
