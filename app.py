from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = Flask(__name__)

def google_dork_search(title, filetype):
    # Monta a URL de pesquisa do Google
    search_url = f"https://www.google.com/search?q=intitle:{urllib.parse.quote(title)}+filetype:{urllib.parse.quote(filetype)}"
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

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        filetype = request.form['filetype']
        results = google_dork_search(title, filetype)
        return render_template('results.html', results=results)
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
