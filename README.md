# 🚀 Extrator de Dados de PDF para Excel

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://extrator-pdf-aero.streamlit.app/)

## 💡 A História por Trás do Projeto

Este projeto nasceu de uma necessidade real: ajudar meu irmão em seu trabalho. Uma de suas tarefas era extrair manualmente informações de centenas de Declarações de Importação em formato PDF e consolidá-las em uma única planilha, um processo repetitivo e cansativo que podia levar um dia inteiro de trabalho.

Para resolver isso, criei esta aplicação. O que antes era um dia de trabalho manual, agora é resolvido com um único clique, otimizando o tempo e eliminando o risco de erros humanos.

![Demonstração da Aplicação](demonstracao.gif) 

```mermaid
%% Diagrama de Fluxo para o projeto extrator-pdf-streamlit
%% Versão Simplificada - Corrigido por Gemini

graph TD;
    subgraph "Interface do Usuário (Navegador Web)"
        A[Início: Usuário acessa a URL da aplicação] --> B["Clique em 'Faça o upload do seu arquivo'"];
        B --> C[/Upload do Arquivo PDF/];
        C --> D{Aguardando processamento...};
        H --> I[Fim: Visualiza o texto extraído <br/> de cada página em seções separadas];
    end

    subgraph "Backend da Aplicação (Servidor Streamlit)"
        C --> E[app.py recebe o arquivo PDF];
        E --> F["PyPDF2 abre o documento <br/> e conta o número de páginas"];
        F --> G{Loop: Para cada página no PDF...};
        G --Página N--> H["Extrai o texto e o exibe <br/> dentro de um `st.expander`"];
        G --Fim do Loop--> H;
    end
```

## ✨ Funcionalidades

-   **Otimização de Tempo:** Transforma uma tarefa de um dia inteiro em um processo de segundos.
-   **Upload Múltiplo:** Faça o upload de um ou vários arquivos PDF de uma só vez.
-   **Extração Inteligente:** Utiliza expressões regulares (Regex) para encontrar e extrair dados específicos dos documentos, como "D.I.", "Nome do Processo", "INVOICE" e "HAWB".
-   **Visualização Instantânea:** Os dados extraídos são exibidos em uma tabela interativa na própria aplicação.
-   **Download Fácil:** Com um único clique, baixe o relatório completo e consolidado em formato `.xlsx` (Excel).
-   **Interface Amigável:** Criada com Streamlit para ser intuitiva e fácil de usar, mesmo para pessoas sem conhecimento técnico.

## ⚙️ Tecnologias Utilizadas

-   **Python:** A linguagem base do projeto.
-   **Streamlit:** Para a criação da interface web interativa.
-   **Pandas:** Para a estruturação e manipulação dos dados.
-   **PyMuPDF (fitz):** Para a leitura e extração de texto dos arquivos PDF.
-   **XlsxWriter:** Motor para a criação do arquivo Excel final.

## 👨‍💻 Como Usar a Aplicação Online

1.  **Acesse a aplicação** através do link: [https://extrator-pdf-aero.streamlit.app/](https://extrator-pdf-aero.streamlit.app/)
2.  **Faça o upload dos arquivos:** Clique no botão "Browse files" e selecione todos os arquivos PDF que deseja processar.
3.  **Processe os dados:** Após o upload, clique no botão "▶️ Processar Arquivos e Gerar Relatório".
4.  **Visualize e Baixe:** A tabela com os dados aparecerá na tela. Logo abaixo, clique no botão "📥 Baixar Relatório em Excel" para obter seu arquivo consolidado.

## 🛠️ Configuração do Ambiente Local (Para Desenvolvedores)

Se você quiser rodar este projeto na sua própria máquina para fazer modificações:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/mulinco/extrator-pdf-streamlit.git](https://github.com/mulinco/extrator-pdf-streamlit.git)
    cd extrator-pdf-streamlit
    ```

2.  **Crie e ative um ambiente virtual** (recomendado):
    ```bash
    # Para Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # Para macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências** a partir do arquivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Rode a aplicação Streamlit:**
    ```bash
    streamlit run app.py
    ```
    A aplicação abrirá automaticamente no seu navegador.

## 🔮 Possíveis Melhorias Futuras

-   Melhorar as expressões regulares (Regex) para cobrir mais variações de layouts de PDF.
-   Adicionar suporte a arquivos PDF baseados em imagem, utilizando OCR (Optical Character Recognition) com bibliotecas como `pytesseract`.
-   Implementar uma opção para se conectar a uma pasta do Google Drive e processar os arquivos de lá.
-   Adicionar testes unitários para garantir a precisão da extração.

## 📄 Licença

Distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais informações.
