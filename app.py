import streamlit as st

# Importando os componentes das abas
from components.tab_processamento import show_tab_processamento
from components.tab_instrucoes import show_tab_instrucoes
from components.tab_contato import show_tab_contato

# ===================================================================
# CONFIGURAÇÃO DA PÁGINA 
# ===================================================================
st.set_page_config(
    page_title="Extrator de Dados PDF",
    layout="wide",
    page_icon="assets/aeroimport-logo.png" # Certifique-se que o caminho está certo
)

# ===================================================================
# FUNÇÕES DE UI (Login e Main App)
# ===================================================================

def show_login_form():
    """Mostra o formulário de login."""
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>🔒 Acesso Restrito</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Por favor, insira a senha para utilizar a ferramenta.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        password = st.text_input(
            "Senha", 
            type="password", 
            key="password_input",
            label_visibility="collapsed"
        )
        if st.button("Entrar", use_container_width=True):
            if password == st.secrets.get("APP_PASSWORD", ""):
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Senha incorreta.")

def show_main_app():
    """Mostra a aplicação principal após o login."""
    
    # --- Header e Logout ---
    with st.container():
        col_msg, col_btn = st.columns([8, 1])
        col_msg.write("Bem-vindo! Você está logado.")
        if col_btn.button("Logout", key="logout_button"):
            st.session_state['logged_in'] = False
            st.rerun()
    
    st.markdown("---")
    st.title("🤖 Ferramenta de Extração de Dados - D.I.")

    # Cria as abas
    tab1, tab2, tab3 = st.tabs(["📤 Upload e Processamento", "❓ Como Usar", "🐞 Relatar Bug"])

    # Chama os componentes para renderizar o conteúdo em cada aba
    with tab1:
        show_tab_processamento()
    
    with tab2:
        show_tab_instrucoes()

    with tab3:
        show_tab_contato()

# ===================================================================
# LÓGICA PRINCIPAL (ROTEADOR)
# ===================================================================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    show_main_app()
else:
    show_login_form()