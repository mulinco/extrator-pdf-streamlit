import streamlit as st
import pandas as pd
import fitz # PyMuPDF
import re
import io

# =================================================================================
# FUNÇÃO DE EXTRAÇÃO ESPECÍFICA PARA ESTA FERRAMENTA
# =================================================================================
# Dentro do seu arquivo pages/3_Fechamento_Aeronave.py

# Substitua sua função extract_fechamento_data por esta:

def extract_fechamento_data(uploaded_file):
    """
    Versão final e robusta, construída a partir dos dados reais do PDF.
    """
    file_name = uploaded_file.name
    
    data = {
        "Processo": None,
        "Aeronave": "MANUTENÇÃO DE FROTA",
        "Invoice": None,
        "HAWB": None,
        "Nome do Arquivo PDF": file_name
    }

    try:
        pdf_bytes = uploaded_file.getvalue()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        texto_completo = ""
        # Junta o texto das primeiras 5 páginas para uma busca global e mais segura
        for i in range(min(len(doc), 5)):
            texto_completo += doc[i].get_text("text") + "\n"
        
        # --- Lógica de extração com regras refinadas ---

        # Busca por Processo (Nossa Referencia)
        match_processo = re.search(r'Nossa Referencia[\s\.]*:\s*(\S+)', texto_completo, re.IGNORECASE)
        if match_processo:
            data["Processo"] = match_processo.group(1).strip()

        # Busca por Invoice (lida com quebra de linha na palavra-chave)
        match_invoice = re.search(r'Fatura\s*Comerci\s*al[\s\.]*:\s*(\S+)', texto_completo, re.IGNORECASE)
        if match_invoice:
            data["Invoice"] = match_invoice.group(1).strip()

        # Busca por HAWB
        match_hawb = re.search(r'HAWB[\s\.]*:\s*(\S+)', texto_completo, re.IGNORECASE)
        if match_hawb:
            data["HAWB"] = match_hawb.group(1).strip()

        # Busca pela sigla da Aeronave (regra específica e precisa)
        # Procura pela palavra AERONAVE seguida por um código no formato XX-XXX
        match_aeronave = re.search(r'\bAERONAVE\s+([A-Z]{2,3}-[A-Z]{3})\b', texto_completo, re.IGNORECASE)
        if match_aeronave:
            data["Aeronave"] = match_aeronave.group(1).strip()
            
        doc.close()
    except Exception as e:
        st.warning(f"Erro ao processar o PDF '{file_name}': {e}")
    
    return data
# =================================================================================
# VERIFICAÇÃO DE LOGIN - O "GUARDA" DA PÁGINA
# =================================================================================
st.set_page_config(page_title="Fechamento Aeronave", page_icon="✈️")

if not st.session_state.get('logged_in', False):
    st.error("Acesso negado. Por favor, faça o login na página 'Login'.")
    st.stop()
# =================================================================================

# --- INTERFACE DA NOVA FERRAMENTA ---
st.title("✈️ Ferramenta de Fechamento - Aeronave")
st.markdown("Faça o upload dos PDFs para extrair os dados de **Processo, Aeronave, Invoice e HAWB**.")
st.markdown("---")


uploaded_files = st.file_uploader(
    "Selecione os arquivos PDF para esta extração",
    type="pdf",
    accept_multiple_files=True,
    key="file_uploader_aeronave" # Chave única para este uploader
)

if uploaded_files:
    if st.button("▶️ Extrair Dados de Fechamento", use_container_width=True):
        with st.spinner("Analisando documentos... Por favor, aguarde."):
            
            extracted_records = []
            for pdf_file in uploaded_files:
                record = extract_fechamento_data(pdf_file)
                if record:
                    extracted_records.append(record)

            if extracted_records:
                st.header("Resultados da Extração")
                df_final = pd.DataFrame(extracted_records)
                
                # Garante a ordem exata das colunas que você pediu
                output_columns_order = ["Processo", "Aeronave", "Invoice", "HAWB", "Nome do Arquivo PDF"]
                df_final = df_final[output_columns_order]
                
                st.dataframe(df_final)

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_final.to_excel(writer, index=False, sheet_name='Fechamento_Aeronave')
                
                st.download_button(
                    label="📥 Baixar Planilha de Fechamento",
                    data=output.getvalue(),
                    file_name="Planilha_Fechamento_Aeronave.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("Nenhum dado relevante foi extraído dos arquivos fornecidos.")