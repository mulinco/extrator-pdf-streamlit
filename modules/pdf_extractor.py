import fitz  # PyMuPDF
import re
import streamlit as st

def extract_di_data(uploaded_file):
    """
    Recebe um arquivo PDF (UploadFile do Streamlit) e retorna um dicionário com os dados extraídos.
    """
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
        # Abre o PDF a partir dos bytes em memória
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
        return data

    except Exception as e:
        st.warning(f"Erro ao processar o PDF '{uploaded_file.name}': {e}")
        return None

def extract_fechamento_data(uploaded_file):
    """
    Versão final e robusta para Fechamento de Aeronave.
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
        # Junta o texto das primeiras 5 páginas
        for i in range(min(len(doc), 5)):
            texto_completo += doc[i].get_text("text") + "\n"
        
        # --- Lógica de extração ---

        # Busca por Processo
        match_processo = re.search(r'Nossa Referencia[\s\.]*:\s*(\S+)', texto_completo, re.IGNORECASE)
        if match_processo:
            data["Processo"] = match_processo.group(1).strip()

        # Busca por Invoice
        match_invoice = re.search(r'Fatura\s*Comerci\s*al[\s\.]*:\s*(\S+)', texto_completo, re.IGNORECASE)
        if match_invoice:
            data["Invoice"] = match_invoice.group(1).strip()

        # Busca por HAWB
        match_hawb = re.search(r'HAWB[\s\.]*:\s*(\S+)', texto_completo, re.IGNORECASE)
        if match_hawb:
            data["HAWB"] = match_hawb.group(1).strip()

        # Busca pela Aeronave
        match_aeronave = re.search(r'\bAERONAVE\s+([A-Z]{2,3}-[A-Z]{3})\b', texto_completo, re.IGNORECASE)
        if match_aeronave:
            data["Aeronave"] = match_aeronave.group(1).strip()
            
        doc.close()
        return data

    except Exception as e:
        st.warning(f"Erro ao processar o PDF '{file_name}': {e}")
        return None