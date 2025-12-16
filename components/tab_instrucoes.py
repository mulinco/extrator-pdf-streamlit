import streamlit as st

def show_tab_instrucoes():
    """
    Renderiza o conteúdo da aba de Instruções.
    """
    st.header("Como usar a ferramenta")
    st.info("""
    1.  Vá para a aba **"📤 Upload e Processamento"**.
    
    2.  Clique no botão **"Browse files"** ou simplesmente arraste todos os arquivos PDF que você deseja analisar para a área de upload.
    
    3.  Uma vez que os arquivos estejam listados, clique no botão azul **"▶️ Processar Arquivos e Gerar Relatório"**.
    
    4.  Aguarde um momento enquanto a ferramenta lê os documentos. A tabela com os dados extraídos aparecerá na tela.
    
    5.  Por fim, clique em **"📥 Baixar Relatório em Excel"** para salvar a planilha final no seu computador.
    """)