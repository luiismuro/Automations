import requests
import time
import csv
import random
import concurrent.futures
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

MAX_THREADS = 10
def extract_movie_details(movie_link):
    time.sleep(random.uniform(0, 0.5))  # Pequena pausa para não sobrecarregar o servidor
    try:
        # Realiza a requisição para a página do filme
        response = requests.get(movie_link, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extração de dados
        title = None
        date = None
        rating = None
        plot_text = None

        movie_data = soup.find('div', class_='ipc-title__text')
        if movie_data:
            title = movie_data.find('h3').get_text(strip=True)
        
        rating_element = soup.find('span', itemprop='ratingValue')
        rating = rating_element.get_text(strip=True) if rating_element else 'N/A'

        plot_element = soup.find('div', class_='summary_text')
        plot_text = plot_element.get_text(strip=True) if plot_element else 'N/A'

        # Salvando os dados no CSV
        if all([title, date, rating, plot_text]):
            with open('movies.csv', mode='a', newline='') as file:
                writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([title, date, rating, plot_text])
                print(f'Salvo: {title}, {date}, {rating}, {plot_text}')

    except Exception as e:
        print(f"Erro ao processar {movie_link}: {e}")

def extract_movies(soup):
    # Encontra a tabela de filmes
    movies_table = soup.find('table', attrs={'data-caller-name': 'chart-moviemeter'}).find('tbody')
    movies_table_rows = movies_table.find_all('tr')

    # Cria a lista de links dos filmes
    movie_links = ['https://imdb.com' + row.find('a')['href'] for row in movies_table_rows]

    # Usa multithreading para melhorar o desempenho
    threads = min(MAX_THREADS, len(movie_links))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(extract_movie_details, movie_links)

def main():
    start_time = time.time()

    # URL dos filmes populares no IMDB
    popular_movies_url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
    
    # Faz a requisição para a página principal
    response = requests.get(popular_movies_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Função para extrair os filmes populares
    extract_movies(soup)

    end_time = time.time()
    print(f'Tempo total: {end_time - start_time:.2f} segundos')

if __name__ == '__main__':
    # Cria o arquivo CSV e escreve o cabeçalho
    with open('movies.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Título', 'Data de lançamento', 'Avaliação', 'Resumo'])

    # Executa o processo principal
    main()