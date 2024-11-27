import requests
import csv
import time
from bs4 import BeautifulSoup
import concurrent.futures
from threading import Lock

# Configuração do cabeçalho para simular navegador
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}

# URL dos filmes populares no IMDb
IMDB_URL = "https://www.imdb.com/chart/moviemeter/"
CSV_FILE = 'movies.csv'

# Lock para escrita segura no CSV
lock = Lock()

# Função para extrair detalhes de um único filme
def extract_movie_data(item):
    try:
        # Extraindo título
        title_tag = item.find('h3', class_='ipc-title__text')
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        # Extraindo link
        link_tag = item.find('a', href=True)
        link = f"https://www.imdb.com{link_tag['href']}" if link_tag else "N/A"

        # Extraindo ano
        year_tag = item.find('span', class_='sc-6ade9358-7')
        year = year_tag.get_text(strip=True) if year_tag else "N/A"

        # Extraindo avaliação
        rating_tag = item.find('span', class_='ipc-rating-star--rating')
        rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"

        return [title, year, rating, link]
    except Exception as e:
        print(f"Erro ao processar filme: {e}")
        return ["N/A", "N/A", "N/A", "N/A"]

# Função single-threaded
def extract_movies_single_threaded(soup):
    print("Extraindo filmes (single-threaded)...")
    start_time = time.time()
    movie_items = soup.find_all('li', class_='ipc-metadata-list-summary-item')
    movies = [extract_movie_data(item) for item in movie_items]
    save_to_csv(movies)
    print(f"Concluído em {time.time() - start_time:.2f} segundos.")
    return movies

# Função multi-threaded
def extract_movies_multi_threaded(soup):
    print("Extraindo filmes (multi-threaded)...")
    start_time = time.time()
    movie_items = soup.find_all('li', class_='ipc-metadata-list-summary-item')
    movies = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(extract_movie_data, movie_items))
        movies.extend(results)

    save_to_csv(movies)
    print(f"Concluído em {time.time() - start_time:.2f} segundos.")
    return movies

# Função para salvar no CSV
def save_to_csv(movies):
    with lock:
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Título', 'Ano', 'Avaliação', 'Link'])
            writer.writerows(movies)
    print("Filmes salvos em 'movies.csv' com sucesso!")

# Função principal
def main(use_threads=False):
    print("Iniciando extração...")
    response = requests.get(IMDB_URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Erro ao acessar o site: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    if use_threads:
        extract_movies_multi_threaded(soup)
    else:
        extract_movies_single_threaded(soup)

if __name__ == "__main__":
    # Execução com medição de tempo
    print("---- Versão Single-threaded ----")
    main(use_threads=False)
    
    print("\n---- Versão Multi-threaded ----")
    main(use_threads=True)
