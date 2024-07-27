import requests
from bs4 import BeautifulSoup
import urllib.parse

def google_dork_search(query, filetype):
    # Monta a URL de pesquisa do Google
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}+filetype:{urllib.parse.quote(filetype)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Envia a solicitação HTTP
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        raise Exception("Erro ao realizar a busca no Google")

    # Analisa o HTML da página de resultados
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontra os links dos resultados de pesquisa
    results = []
    for g in soup.find_all('div', class_='g'):
        link = g.find('a')
        if link and link['href']:
            results.append(link['href'])

    return results

if __name__ == "__main__":
    dork_query = input("Insira sua consulta de Google Dork: ")
    filetype = input("Insira o formato de arquivo (por exemplo, pdf, docx, etc.): ")
    results = google_dork_search(dork_query, filetype)
    for result in results:
        print(result)
