import streamlit as st
import pandas as pd
import io
from modules.pdf_extractor import extract_di_data

def show_tab_processamento():
    """
    Renderiza todo o conteúdo da aba de Upload e Processamento.
    """
    st.header("Passo 1: Faça o upload dos arquivos")
    
    uploaded_files = st.file_uploader(
        "Selecione um ou mais arquivos PDF",
        type="pdf",
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="uploader_processamento" # Key única para evitar conflitos
    )

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
                    # Filtra apenas colunas que existem para evitar erro
                    cols_to_use = [col for col in output_columns_order if col in df_final.columns]
                    df_final = df_final[cols_to_use]
                    
                    st.dataframe(df_final)

                    # Cria o arquivo Excel em memória
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        df_final.to_excel(writer, index=False, sheet_name='Declaracoes')
                    
                    st.download_button(
                        label="📥 Baixar Relatório em Excel",
                        data=output.getvalue(),
                        file_name="Relatorio_Extracao.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.warning("Nenhum dado foi extraído dos arquivos fornecidos. Verifique o formato dos PDFs.")