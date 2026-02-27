import uuid  # Mantido para evitar o erro interno da biblioteca DuckDuckGo
import streamlit as st
import pandas as pd # Necessário para processar o CSV
from langchain_ollama import ChatOllama
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage

# ==========================================
# 1. Configurações da Página e Estilo
# ==========================================
st.set_page_config(page_title="Agente Local Felipe", page_icon="🤖", layout="wide")

st.markdown("""
<style>
/* Fundo geral */
.stApp { background: linear-gradient(135deg, #0f172a, #020617); }

/* Centralizar chat */
.main { max-width: 900px; margin: auto; }
            
/* FOCO AQUI: Aumentar apenas as respostas do Agente */
[data-testid="stChatMessage"][data-testid*="assistant"] {
    background-color: #0ea5e9;
    border-radius: 15px;
    padding: 15px;
    margin: 10px 0;
    font-size: 22px; /* Altere este valor para o tamanho que desejar */
}            

/* Bolha usuário */
[data-testid="stChatMessage"][data-testid*="user"] {
    background-color: #1e293b;
    border-radius: 15px;
    padding: 15px;
    margin: 10px 0;
    font-size: 26px; /* Tamanho aumentado conforme solicitado */
}

/* Bolha assistente */
[data-testid="stChatMessage"][data-testid*="assistant"] {
    background-color: #0ea5e9;
    border-radius: 15px;
    padding: 15px;
    margin: 10px 0;
    font-size: 26px; /* Tamanho aumentado conforme solicitado */
}

/* Campo de entrada de texto */
.stChatInput textarea {
    font-size: 22px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] { background-color: #020617; }

/* Botão */
.stButton button {
    width: 100%;
    border-radius: 10px;
    background-color: #0ea5e9;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 Meu Agente IA Local")
st.markdown("Desenvolvido com Python, LangChain e Ollama.")

def analisar_estatisticas_csv(df):
    """Gera um resumo estatístico das colunas numéricas do DataFrame."""
    if df is not None:
        # describe() gera contagem, média, desvio padrão, min, max e quartis
        resumo = df.describe().to_string()
        return f"Aqui está a análise estatística das colunas numéricas:\n\n{resumo}"
    return "Nenhum ficheiro CSV foi carregado para análise."

# ==========================================
# 2. Inicialização do Agente (Cache para performance)
# ==========================================
@st.cache_resource
def init_agent():
    llm = ChatOllama(model="llama3.2", temperature=0)
    search = DuckDuckGoSearchRun()
    
    # Usando o wrapper para evitar erros de inspeção de tipo
    tools = [
        DuckDuckGoSearchRun(name="busca_internet", description="Pesquisa fatos atuais na internet")
    ]
    
    return create_react_agent(model=llm, tools=tools)

agent = init_agent()

# ==========================================
# 3. Sidebar: Upload de CSV e Controles
# ==========================================
with st.sidebar:
    st.header("📂 Gerenciar Dados")
    arquivo_csv = st.file_uploader("Carregue um arquivo CSV", type=["csv"])
    
    contexto_csv = ""
    if arquivo_csv:
        try:
            df = pd.read_csv(arquivo_csv)
            st.success("CSV carregado com sucesso!")
            st.write("### Prévia dos Dados:")
            st.dataframe(df.head(5)) # Mostra as primeiras 5 linhas na sidebar
            
            # Criamos uma string de contexto com informações do arquivo
            colunas = ", ".join(df.columns)
            dados_amostra = df.head(10).to_string()
            contexto_csv = f"\n\n[CONTEXTO DO ARQUIVO CSV]\nColunas: {colunas}\nPrimeiras 10 linhas:\n{dados_amostra}"
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")

    if st.button("Limpar Histórico"):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# 4. Gerenciamento do Histórico de Chat
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message("user" if isinstance(msg, HumanMessage) else "assistant"):
        st.markdown(msg.content)

# ==========================================
# 5. Input e Execução
# ==========================================
if prompt := st.chat_input("Como posso ajudar hoje?"):
    
    if ("estatística" in prompt.lower() or "resumo" in prompt.lower()) and arquivo_csv:
        stats_context = analisar_estatisticas_csv(df)
        prompt_final = f"{prompt}\n\nUtiliza estes dados estatísticos para a tua resposta: {stats_context}"
    else:
        prompt_final = f"{prompt}{contexto_csv}" if contexto_csv else prompt

   
    
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analisando informações..."):
            try:
                
                resultado = agent.invoke({"messages": [HumanMessage(content=prompt_final)]})
                resposta_final = resultado["messages"][-1].content
                
                st.markdown(resposta_final)
                st.session_state.messages.append(AIMessage(content=resposta_final))
            except Exception as e:
                st.error(f"Erro ao processar: {e}")