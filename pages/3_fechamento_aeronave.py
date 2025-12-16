import streamlit as st
import pandas as pd
import io
from modules.pdf_extractor import extract_fechamento_data


# CONFIGURAÇÃO E LOGIN

st.set_page_config(page_title="Fechamento Aeronave", page_icon="✈️")

if not st.session_state.get('logged_in', False):
    st.error("Acesso negado. Por favor, faça o login na página principal.")
    st.stop()


# INTERFACE VISUAL

st.title("✈️ Ferramenta de Fechamento - Aeronave")
st.markdown("Faça o upload dos PDFs para extrair os dados de **Processo, Aeronave, Invoice e HAWB**.")
st.markdown("---")

uploaded_files = st.file_uploader(
    "Selecione os arquivos PDF",
    type="pdf",
    accept_multiple_files=True,
    key="file_uploader_aeronave"
)

if uploaded_files:
    if st.button("▶️ Extrair Dados", use_container_width=True):
        with st.spinner("Analisando documentos... Por favor, aguarde."):
            
            extracted_records = []
            for pdf_file in uploaded_files:
                # Chama a função que agora vive no modules/pdf_extractor.py
                record = extract_fechamento_data(pdf_file)
                if record:
                    extracted_records.append(record)

            if extracted_records:
                st.header("Resultados da Extração")
                df_final = pd.DataFrame(extracted_records)
                
                # Ordenação das colunas
                output_columns_order = ["Processo", "Aeronave", "Invoice", "HAWB", "Nome do Arquivo PDF"]
                # Garante que as colunas existem antes de reordenar para evitar erro
                cols_to_use = [col for col in output_columns_order if col in df_final.columns]
                df_final = df_final[cols_to_use]
                
                st.dataframe(df_final)

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_final.to_excel(writer, index=False, sheet_name='Fechamento_Aeronave')
                
                st.download_button(
                    label="📥 Baixar Planilha",
                    data=output.getvalue(),
                    file_name="Planilha_Fechamento_Aeronave.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("Nenhum dado relevante foi extraído dos arquivos fornecidos.")