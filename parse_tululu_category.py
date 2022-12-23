import argparse
import json
import logging
import os

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

from functions import check_for_redirect, download_txt, download_image,\
    parse_book_page


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Скачивание книг с сайта tululu')
    parser.add_argument('--start_page', help='Начало диапазона страниц для скачивания книг', nargs='?', type=int, default=1)
    parser.add_argument('--end_page', help='Конец диапазона страниц для скачивания книг', nargs='?', type=int, default=702)
    parser.add_argument('--dest_folder', help='Путь к каталогу с картинками и книгами', nargs='?', default='.')
    parser.add_argument('--skip_imgs', help='Не скачивать картинки', action="store_true")
    parser.add_argument('--skip_txt', help='Не скачивать книги', action="store_true")
    parser.add_argument('--json_path', help='Путь к json', nargs='?', default='.')
    args = parser.parse_args()
    
    books = []
    for page in range(args.start_page, args.end_page):
        try:
            category_url = f'https://tululu.org/l55/{page}'
            response = requests.get(category_url)
            response.raise_for_status()
            check_for_redirect(response)
            
            soup = BeautifulSoup(response.text, 'lxml')
            selector = 'div.bookimage'
            books_block = soup.select(selector)
            for book_block in books_block:
                selector = 'a'
                book_href = book_block.select_one(selector)['href']
                
                book_page_url = urljoin(category_url, book_href)
                response = requests.get(book_page_url)
                response.raise_for_status()
                check_for_redirect(response)
                
                book = parse_book_page(response.text, book_page_url)
                
                if not args.skip_txt:
                    filename = f'{book["title"]}.txt'
                    url = 'https://tululu.org/txt.php'
                    book_id = ''.join(filter(str.isnumeric, book_href))
                    book_filename = download_txt(url, filename, book_id, f'{args.dest_folder}/books/')
                    book['book_path'] = f'{args.dest_folder}/books/{book_filename}'
                
                if not args.skip_imgs:
                    download_image(book['image_url'], book['image_name'], f'{args.dest_folder}/images/')
                
                books.append(book)
                
            
        except requests.ConnectionError:
            logging.info('Проблема подключения. Повторная попытка через 60 секунд.')
            time.sleep(60)
            continue
        except requests.HTTPError:
            logging.info(f'Запрашиваемой страницы нет на сайте.')
    
    books_json = json.dumps(books, indent=4)
    os.makedirs(args.json_path, exist_ok=True)
    with open(f'{args.json_path}/books.json', 'w', encoding='utf8') as file:
        json.dump(books, file, ensure_ascii=False, indent=4)
        file.write(books_json)