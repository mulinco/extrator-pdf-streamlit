import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import re
import io

# --------------------------------------------------------------------------
# A função de extração agora recebe o objeto de arquivo do Streamlit
# e abre o PDF diretamente da memória, o que é mais eficiente.
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
        st.warning(f"Erro ao processar o PDF '{file_name}': {e}")
    
    return data
# --------------------------------------------------------------------------


# --- Interface do Streamlit ---
st.set_page_config(page_title="Extrator de Dados de PDF", layout="wide")
st.title("🤖 Extrator de Dados de Declarações de Importação")
st.markdown("Faça o upload dos arquivos PDF do seu computador para extrair as informações e gerar um relatório em Excel.")

# --- Componente de Upload ---
# Este é o coração da nova versão.
uploaded_files = st.file_uploader(
    "Selecione um ou mais arquivos PDF",
    type="pdf",
    accept_multiple_files=True
)

# O código só continua se o usuário tiver feito upload de algum arquivo
if uploaded_files:
    st.info(f"{len(uploaded_files)} arquivo(s) selecionado(s).")
    
    # Botão para iniciar o processamento dos arquivos que já foram carregados
    if st.button("▶️ Processar Arquivos e Gerar Relatório"):
        try:
            with st.spinner("Extraindo dados dos PDFs... Isso pode levar um momento."):
                extracted_records = []
                progress_bar = st.progress(0)
                
                for i, pdf_file in enumerate(uploaded_files):
                    record = extract_di_data(pdf_file)
                    extracted_records.append(record)
                    progress_bar.progress((i + 1) / len(uploaded_files), text=f"Processando: {pdf_file.name}")

            # Criação e Exibição do DataFrame
            df_final = pd.DataFrame(extracted_records)
            
            # Garante a ordem correta das colunas
            output_columns_order = ["D.I.", "Nome do Processo", "INVOICE", "HAWB", "Nome do Arquivo PDF"]
            df_final = df_final.reindex(columns=output_columns_order)
            
            st.success("Dados extraídos com sucesso!")
            st.dataframe(df_final)

            # Botão de Download do Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_final.to_excel(writer, index=False, sheet_name='Declaracoes')
            
            st.download_button(
                label="📥 Baixar Relatório em Excel",
                data=output.getvalue(),
                file_name="Controle_de_Declaracoes_Importacao.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"Ocorreu um erro durante o processo: {e}")