import json
import logging

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

from functions import check_for_redirect, download_txt, download_image,\
    parse_book_page


if __name__ == '__main__':
    books = []
    for page in range(1,5):
        try:
            url = f'https://tululu.org/l55/{page}'
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            books_block = soup.find_all('div', class_='bookimage')
            for book_block in books_block:
                book_href = book_block.find('a')['href']
                
                url = urljoin('https://tululu.org', book_href)
                response = requests.get(url)
                response.raise_for_status()
                check_for_redirect(response)
                
                book = parse_book_page(response.text, url)
                
                filename = f'{book["title"]}.txt'
                url = 'https://tululu.org/txt.php'
                book_id = book_href.replace('/', '')
                book_filename = download_txt(url, filename, book_id)
                book['book_path'] = f'books/{book_filename}'
                
                download_image(book['image_url'], book['image_name'])
                
                books.append(book)
                
            
        except requests.ConnectionError:
            logging.info('Проблема подключения. Повторная попытка через 60 секунд.')
            time.sleep(60)
            continue
        except requests.HTTPError:
            logging.info(f'Страницы {url} нет на сайте.')
    
    # books_json = json.dumps(books, indent=4)
    with open('books.json', 'w', encoding='utf8') as file:
        json.dump(books, file, ensure_ascii=False, indent=4)
        # file.write(books_json)