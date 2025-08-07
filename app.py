import streamlit as st
import pandas as pd
import fitz # PyMuPDF
import re
import io
import requests

# ===================================================================
# CONFIGURAÇÃO DA PÁGINA 
# ===================================================================
st.set_page_config(
    page_title="Extrator de Dados PDF",
    layout="wide",
    page_icon="aeroimport-logo.png"
)

# ===================================================================
# FUNÇÕES DO APLICATIVO
# ===================================================================



def send_telegram_message(message_text):
    """Função para enviar uma mensagem para o seu Telegram via Bot."""
    bot_token = st.secrets.get("telegram", {}).get("BOT_TOKEN")
    chat_id = st.secrets.get("telegram", {}).get("CHAT_ID")

    if not bot_token or not chat_id:
        st.error("Credenciais do Telegram não configuradas nos Secrets.")
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, json=payload)
        return response.json().get("ok", False)
    except Exception as e:
        st.error(f"Erro ao enviar a mensagem: {e}")
        return False

def extract_di_data(uploaded_file):
    # O nome do arquivo vem diretamente do objeto de upload
    file_name = uploaded_file.name
    
    data = {
        "D.I.": None,
        "Nome do Processo": None,
        "INVOICE": None,
        "HAWB": None,
        "Nome do Arquivo PDF": file_name
    }

    try:
        # Abre o PDF a partir dos bytes em memória, sem salvar em disco
        pdf_bytes = uploaded_file.getvalue()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        # Extração da Página 1
        if len(doc) >= 1:
            page_1_text = doc[0].get_text()
            match_di_num = re.search(r'Declaração:\s*([A-Za-z0-9\-\_/]+)', page_1_text, re.IGNORECASE | re.DOTALL)
            if match_di_num:
                data["D.I."] = match_di_num.group(1).strip()

        # Extração da Página 2
        if len(doc) >= 2:
            page_2_text = doc[1].get_text()
            match_ref = re.search(r'Nossa Referencia[\s\.]*:\s*([A-Za-z0-9\-\_]+)', page_2_text, re.IGNORECASE | re.DOTALL)
            if match_ref:
                data["Nome do Processo"] = match_ref.group(1).strip()

            match_invoice = re.search(r'(?:Fatura Comercial|\bFatura Comerci\s*\n\s*al|\bFatura\s*\n\s*Comercial)[\s\.:]*([A-Za-z0-9\-\_\,\s]+?)(?=\s*(?:MAWB|HAWB|$))', page_2_text, re.IGNORECASE | re.DOTALL)
            if match_invoice:
                data["INVOICE"] = match_invoice.group(1).strip()

            match_hawb = re.search(r'HAWB[\s\.]*:\s*([A-Za-z0-9\-\_]+)', page_2_text, re.IGNORECASE | re.DOTALL)
            if match_hawb:
                data["HAWB"] = match_hawb.group(1).strip()
        
        doc.close()
    except Exception as e:
        st.warning(f"Erro ao processar o PDF '{uploaded_file.name}': {e}")
    
    return data

def show_main_app():
    """Mostra a aplicação principal após o login."""
    
    # Botão de Logout
    with st.container():
        st.write(f"Bem-vindo! Você está logado.")
        if st.button("Logout", key="logout_button"):
            st.session_state['logged_in'] = False
            st.rerun()
    
    st.markdown("---")
    st.title("🤖 Ferramenta de Extração de Dados")

    tab_processamento, tab_instrucoes, tab_contato = st.tabs(["📤 Upload e Processamento", "❓ Como Usar", "🐞 Relatar Bug"])

    # --- Conteúdo da Primeira Aba ---
    with tab_processamento:
        st.header("Passo 1: Faça o upload dos arquivos")
        uploaded_files = st.file_uploader(
        "Selecione um ou mais arquivos PDF",
        type="pdf",
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if uploaded_files:
        st.header("Passo 2: Processe os dados")
        
        # O botão para iniciar o processo
        if st.button("▶️ Processar Arquivos e Gerar Relatório", use_container_width=True):
            
            # --- TODA A LÓGICA DE PROCESSAMENTO FICA AQUI DENTRO ---
            with st.spinner("Analisando os documentos... Por favor, aguarde."):
                
                extracted_records = []
                for pdf_file in uploaded_files:
                    record = extract_di_data(pdf_file)
                    if record:
                        extracted_records.append(record)

                # A verificação e exibição dos resultados também ficam aqui dentro
                if extracted_records:
                    st.header("Passo 3: Baixe seu relatório")
                    df_final = pd.DataFrame(extracted_records)
                    st.dataframe(df_final)

                    # Cria o arquivo Excel em memória
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        df_final.to_excel(writer, index=False, sheet_name='Declaracoes')
                    
                    # Botão de download
                    st.download_button(
                        label="📥 Baixar Relatório em Excel",
                        data=output.getvalue(),
                        file_name="Relatorio_Extracao.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.warning("Nenhum dado foi extraído dos arquivos fornecidos. Verifique o formato dos PDFs.")
    # --- Conteúdo da Segunda Aba ---
    with tab_instrucoes:
        st.header("Como usar a ferramenta")
        st.info("""
        **Siga os passos abaixo:**
        1. Na aba "Upload e Processamento", carregue seus arquivos PDF.
        2. Clique no botão "Processar" para iniciar a extração.
        3. Baixe o relatório em Excel quando estiver pronto.
        """)

    # --- Conteúdo da Terceira Aba ---
    with tab_contato:
        st.markdown("<h2 style='text-align: center;'>Encontrou um problema ou tem uma sugestão?</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Use o formulário abaixo para me enviar uma notificação.</p>", unsafe_allow_html=True)

        # Colunas para centralizar o formulário
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            with st.form(key="contact_form"):
                user_email = st.text_input(
                    "Seu e-mail (opcional)",
                    placeholder="seu.email@exemplo.com"
                )
                message_body = st.text_area(
                    "Mensagem",
                    placeholder="Descreva o erro ou a sua sugestão...",
                    height=200
                )
                submit_button = st.form_submit_button(
                    label='Enviar Notificação',
                    use_container_width=True
                )

                if submit_button:
                     full_message = f"📨 Novo Relato no App Extrator\n"
                full_message += f"========================\n"
                full_message += f"**De:** {user_email if user_email else 'Anônimo'}\n"
                full_message += f"**Mensagem:**\n{message_body}"
                
                with st.spinner("Enviando..."):
                    if send_telegram_message(full_message):
                        st.success("Sua notificação foi enviada com sucesso! Obrigado pelo feedback.")
                    else:
                        st.error("Houve uma falha no envio. Verifique as credenciais ou tente novamente.")
                    st.success("Notificação enviada!")

def show_main_app():
    """Mostra a aplicação principal após o login."""
    with st.container():
        st.write("Bem-vindo! Você está logado.")
        if st.button("Logout", key="logout_button"):
            st.session_state['logged_in'] = False
            st.rerun()
    st.markdown("---")
    st.title("🤖 Ferramenta de Extração de Dados")
    tab_processamento, tab_instrucoes, tab_contato = st.tabs(["📤 Upload e Processamento", "❓ Como Usar", "🐞 Relatar Bug"])
    with tab_processamento:
        st.header("Passo 1: Faça o upload dos arquivos")
        uploaded_files = st.file_uploader("Selecione um ou mais arquivos PDF", type="pdf", accept_multiple_files=True, label_visibility="collapsed")
        if uploaded_files:
            st.header("Passo 2: Processe os dados")
            if st.button("▶️ Processar Arquivos e Gerar Relatório", use_container_width=True):
                with st.spinner("Analisando os documentos... Por favor, aguarde."):
                    extracted_records = []
                    for pdf_file in uploaded_files:
                        record = extract_di_data(pdf_file)
                        if record:
                            extracted_records.append(record)
                    if extracted_records:
                        st.header("Passo 3: Baixe seu relatório")
                        df_final = pd.DataFrame(extracted_records)
                        # Garante a ordem correta das colunas
                        output_columns_order = ["D.I.", "Nome do Processo", "INVOICE", "HAWB", "Nome do Arquivo PDF"]
                        df_final = df_final.reindex(columns=output_columns_order)
                        st.dataframe(df_final)
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                            df_final.to_excel(writer, index=False, sheet_name='Declaracoes')
                        st.download_button(label="📥 Baixar Relatório em Excel", data=output.getvalue(), file_name="Relatorio_Extracao.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    else:
                        st.warning("Nenhum dado foi extraído dos arquivos fornecidos. Verifique o formato dos PDFs.")
    with tab_instrucoes:
        st.header("Como usar a ferramenta")
        st.info("""
    1.  Vá para a aba **"📤 Upload e Processamento"**.
    
    2.  Clique no botão **"Browse files"** ou simplesmente arraste todos os arquivos PDF que você deseja analisar para a área de upload.
    
    3.  Uma vez que os arquivos estejam listados, clique no botão azul **"▶️ Processar Arquivos e Gerar Relatório"**.
    
    4.  Aguarde um momento enquanto a ferramenta lê os documentos. A tabela com os dados extraídos aparecerá na tela.
    
    5.  Por fim, clique em **"📥 Baixar Relatório em Excel"** para salvar a planilha final no seu computador.
    """)
    with tab_contato:
        st.markdown("<h2 style='text-align: center;'>Encontrou um problema ou tem uma sugestão?</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Use o formulário abaixo para me enviar uma notificação.</p>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form(key="contact_form"):
                user_email = st.text_input("Seu e-mail (opcional)", placeholder="seu.email@exemplo.com")
                message_body = st.text_area("Mensagem", placeholder="Descreva o erro ou a sua sugestão...", height=200)
                submit_button = st.form_submit_button(label='Enviar Notificação', use_container_width=True)
                if submit_button:
                    full_message = f"📨 Novo Relato no App Extrator\n========================\n**De:** {user_email if user_email else 'Anônimo'}\n**Mensagem:**\n{message_body}"
                    with st.spinner("Enviando..."):
                        if send_telegram_message(full_message):
                            st.success("Sua notificação foi enviada com sucesso! Obrigado pelo feedback.")
                        else:
                            st.error("Houve uma falha no envio. Verifique as credenciais ou tente novamente.")

def show_login_form():
    """Mostra o formulário de login com todos os elementos centralizados."""
    st.markdown("<h1 style='text-align: center;'>🔒 Acesso Restrito</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Por favor, insira a senha para utilizar a ferramenta.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        password = st.text_input(
            "Senha", 
            type="password", 
            key="password_input",
            placeholder="Digite sua senha aqui",
            label_visibility="collapsed"
        )
        if st.button("Entrar", use_container_width=True):
            if password == st.secrets.get("APP_PASSWORD", ""):
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Senha incorreta.")

# ===================================================================
# LÓGICA PRINCIPAL - O "ROTEADOR" DA PÁGINA
# ===================================================================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    show_main_app()
else:
    show_login_form()