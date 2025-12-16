import fitz  # PyMuPDF
import os

# Define as pastas de entrada e saída
PASTA_ORIGINAIS = "pdfs_originais"
PASTA_SAIDA = "pdfs_para_github"

# Garante que a pasta de saída exista
os.makedirs(PASTA_SAIDA, exist_ok=True)

termos_sensiveis = [
    "OMNI TAXI AEREO S/A",
    "03.670.763/0006-42",
    "LUIZ TENORIO ALVES PEREIRA",
    "021.740.467-76",
    "AIRBUS HELICOPTERS",
    # Telefones
    "(21) 96444-3791",
    # Endereços e outros dados pessoais que você identificar
    "AVENIDA ALMIRANTE JULIO DE SA BIERRENBACH",
    "RODRIGO DUARTE DE FREITAS", "106.031.367-70",
    "ANDRE LUIS DA SILVA", "080.342.997.58",
    "VINICIUS DE MENEZES COSTA", "128.581.117-82",
    "MARIARODRIGUES.UFRJ@GMAIL.COM" # E-mail de exemplo
]


print("Iniciando processo de anonimização...")

# Itera sobre todos os arquivos na pasta de originais
for nome_arquivo in os.listdir(PASTA_ORIGINAIS):
    if nome_arquivo.lower().endswith(".pdf"):
        caminho_original = os.path.join(PASTA_ORIGINAIS, nome_arquivo)
        caminho_saida = os.path.join(PASTA_SAIDA, nome_arquivo)
        
        print(f"Processando '{nome_arquivo}'...")
        
        # Abre o PDF original
        doc = fitz.open(caminho_original)
        
        # Passa por cada página do documento
        for pagina in doc:
            # Passa por cada termo sensível que queremos remover
            for termo in termos_sensiveis:
                # Procura pelo termo na página
                areas_encontradas = pagina.search_for(termo)
                
                # Para cada localização encontrada, adiciona uma tarja preta
                for area in areas_encontradas:
                    pagina.add_redact_annot(area, fill=(0, 0, 0)) # fill=(0,0,0) é a cor preta
        
            # Aplica as tarjas (isso remove o texto por baixo permanentemente)
            pagina.apply_redactions()
            
        # Salva o novo PDF anonimizado na pasta de saída
        doc.save(caminho_saida)
        doc.close()
        print(f"-> '{nome_arquivo}' anonimizado com sucesso!")

print("\nProcesso concluído! Os PDFs anonimizados estão na pasta 'pdfs_para_github'.")