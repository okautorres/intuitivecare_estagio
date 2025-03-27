import requests
import os
import zipfile
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime


base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
operadoras_url = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/"


output_dir = "dados_ans"
os.makedirs(output_dir, exist_ok=True)


current_year = datetime.now().year
years_to_download = [str(current_year), str(current_year - 1)]

def get_subdirectories(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    subdirs = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if a['href'].strip('/').isdigit()]
    return [sub for sub in subdirs if any(year in sub for year in years_to_download)]

def get_file_links(url, extensions=['.csv', '.zip']):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if any(a['href'].endswith(ext) for ext in extensions)]
    print(f"Arquivos encontrados em {url}: {len(links)}")  
    return links

def download_file(url, output_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f"Arquivo baixado: {output_path}")
    else:
        print(f"Erro ao baixar {url}")

def extract_zip_files(directory):
    for file in os.listdir(directory):
        if file.endswith(".zip"):
            zip_path = os.path.join(directory, file)
            extract_path = os.path.join(directory, file.replace(".zip", ""))
            os.makedirs(extract_path, exist_ok=True)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            print(f"Extraído: {zip_path} para {extract_path}")


subdirectories = get_subdirectories(base_url)
for subdir in subdirectories:
    file_links = get_file_links(subdir, extensions=['.csv', '.zip'])
    for file_link in file_links:
        filename = file_link.split("/")[-1]
        output_path = os.path.join(output_dir, filename)
        download_file(file_link, output_path)


file_links = get_file_links(operadoras_url, extensions=['.csv'])
for file_link in file_links:
    filename = file_link.split("/")[-1]
    output_path = os.path.join(output_dir, filename)
    download_file(file_link, output_path)


extract_zip_files(output_dir)

print("Download e extração concluídos.")
