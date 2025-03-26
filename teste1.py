import os
import urllib.request
import zipfile
from html.parser import HTMLParser

class PDFLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.pdf_links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href" and "Anexo" in attr[1]:
                    if attr[1].endswith(".pdf"):
                        self.pdf_links.append(attr[1])

def download_pdfs():
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    html = response.read().decode()

    parser = PDFLinkParser()
    parser.feed(html)
    pdf_links = parser.pdf_links

    if not pdf_links:
        print("Não foi encontrado anexos.")
        return

    base_url = "https://www.gov.br"
    os.makedirs("downloads", exist_ok=True)
    pdf_files = []

    for pdf_url in pdf_links:
        if not pdf_url.startswith("http"):
            pdf_url = base_url + pdf_url
        pdf_name = pdf_url.split("/")[-1]
        pdf_path = os.path.join("downloads", pdf_name)
        try:
            print(f"Baixando {pdf_name}...")
            urllib.request.urlretrieve(pdf_url, pdf_path)
            pdf_files.append(pdf_path)
            print(f"Baixado.")
        except Exception as e:
            print(f"Erro! Não consegui baixar{pdf_url}: {e}")

    zip_name = "downloads/anexos.zip"
    with zipfile.ZipFile(zip_name, "w") as zipf:
        for pdf in pdf_files:
            zipf.write(pdf, os.path.basename(pdf))

    print(f"Os anexos {pdf_files} foram compactados: {zip_name}")

download_pdfs()
