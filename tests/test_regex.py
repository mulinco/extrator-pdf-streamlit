import pytest
import re

# Descobri que o @pytest.fixture cria dados que podem ser reutilizados em vários testes
@pytest.fixture
def texto_pdf_simulado():
    return """
    Declaração: 2302048520
    Nossa Referencia: PROC-12345
    Fatura Comercial: INV-999
    HAWB: HAWB-001
    AERONAVE PR-ABC
    """

# --- TESTES REAIS ---

def test_encontra_di(texto_pdf_simulado):
    padrao = r'Declaração:\s*([A-Za-z0-9\-\_/]+)'
    match = re.search(padrao, texto_pdf_simulado)
    
    assert match is not None
    assert match.group(1) == "2302048520"

def test_encontra_aeronave(texto_pdf_simulado):
    padrao = r'\bAERONAVE\s+([A-Z]{2,3}-[A-Z]{3})\b'
    match = re.search(padrao, texto_pdf_simulado)
    
    assert match is not None
    assert match.group(1) == "PR-ABC"

def test_nao_deve_encontrar_di_se_nao_existir():
    texto_ruim = "Apenas um texto qualquer sem o numero da declaração"
    padrao = r'Declaração:\s*([A-Za-z0-9\-\_/]+)'
    match = re.search(padrao, texto_ruim)
    
    # Assert que deve ser None se não encontrar
    assert match is None