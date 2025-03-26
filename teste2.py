import pdfplumber
import csv
import zipfile
import os

def substituir_abreviacoes(coluna):
    substituicoes = {
        'OD': 'Oftalmologia Diagnóstico',
        'AMB': 'Ambulatorial'
    }
    return substituicoes.get(coluna, coluna)

def extrair_dados_pdf(pdf_path, paginas_por_vez=10):
    with pdfplumber.open(pdf_path) as pdf:
        tabelas = []
        total_paginas = len(pdf.pages)
        
        for i in range(0, total_paginas, paginas_por_vez):
            paginas_desejadas = range(i, min(i + paginas_por_vez, total_paginas))
            for j in paginas_desejadas:
                pagina = pdf.pages[j]
                tabela = pagina.extract_table()
                if tabela:
                    tabelas.extend(tabela)
        return tabelas



def salvar_csv(dados, nome_arquivo):
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for linha in dados:
            linha = [substituir_abreviacoes(item) for item in linha]
            writer.writerow(linha)



def compactar_zip(nome_arquivo_csv, nome_arquivo_zip):
    with zipfile.ZipFile(nome_arquivo_zip, 'w') as zipf:
        zipf.write(nome_arquivo_csv, os.path.basename(nome_arquivo_csv))

def main():
    pasta_downloads = os.path.join(os.getcwd(), 'downloads')
    pdf_path = os.path.join(pasta_downloads, 'Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf') 
    
    nome_arquivo_csv = "rol_procedimentos.csv"
    nome_arquivo_zip = "Teste_KauanTorres.zip"  


    if not os.path.exists(pdf_path):
        print(f"O arquivo {pdf_path} não foi encontrado!")
        return

    print(f"Um momento enquanto o processo é realizado...")
    dados = extrair_dados_pdf(pdf_path)
    

    salvar_csv(dados, nome_arquivo_csv)
    
    compactar_zip(nome_arquivo_csv, nome_arquivo_zip)
    
    print(f" O arquivo zip {nome_arquivo_zip} foi criado com sucesso.")

if __name__ == "__main__":
    main()
