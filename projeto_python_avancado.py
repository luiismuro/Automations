import requests
import time
import csv
import random
import concurrent.futures
from bs4 import BeautifulSoup

# Global Headers - Emulating browsers to avoid being blocked by the website
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
        }

# Defining threads limiting to 10 in order to accelerate the extraction
MAX_THREADS = 10

# Function to extract movie details
def extract_movie_details(movie_link):
    time.sleep(random.uniform(0, 0.2))
    response = requests.get(movie_link, headers=header)
    movie_soup = BeautifulSoup(response.content, 'html.parser')

    if movie_soup is not None:
        title = None
        date = None

        # Locating website specific section
        page_section = movie_soup.find('section', attrs={'class': 'ipc-page-section'})

        if page_section is not None:
            # Locating all divs inside the section
            divs = page_section.find_all('div', recursive=False)

            if len(divs) > 1:
                target_div = divs[1]

                # Locating Movie name
                title_tag = target_div.find('h1')
                if title_tag:
                    title = title_tag.find('span').get_text()
                
                # Locating launch movie date
                date_tag = target_div.find('a', href=lambda href: href and 'releaseinfo' in href)
                if date_tag:
                    date = date_tag.get_text().strip()

                # Locating movie rating
                rating_tag = movie_soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
                rating = rating_tag.get_text() if rating_tag else None

                # Locating movie synopsis
                plot_tag = movie_soup.find('span', attrs={'data-testid': 'plot-xs_to_m'})
                plot_text = plot_tag.get_text().strip() if plot_tag else None

                with open('movies.csv', mode='a', newline='', encoding='utf-8') as file:
                    movie_writer = csv.writer(file, delimiter=',', quotechar ='"', quoting=csv.QUOTE_MINIMAL)
                    if all([title, date, rating, plot_text]):
                        print(title, date, rating, plot_text)
                        movie_writer.writerow([title, date, rating, plot_text])

# Function to extract Movies from table in main website section
def extract_movies(soup):
    movies_table = soup.find('div', attrs={'data-testid': 'chart-layout-main-column'}).find('ul')
    movies_table_rows = movies_table.find_all('li')
    movie_links = ['https://imdb.com' + movie.find('a')['href'] for movie in movies_table_rows]

    # Using threads to process the extractions
    threads = min(MAX_THREADS, len(movie_links))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(extract_movie_details, movie_links)


# Main function
def main():
    start_time = time.time()

    # IMDB Most popular movies - 100 movies
    popular_movies_url = 'https://imdb.com/chart/moviemeter/?href_=nv_mv_mpm'
    response = requests.get(popular_movies_url, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting movies
    extract_movies(soup)

    # Calculating time spent in the process
    end_time = time.time()
    print('Total time: ', end_time - start_time)

if __name__ == '__main__':
    main()