import argparse
import logging

import requests

from functions import check_for_redirect, download_txt, download_image,\
    parse_book_page


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Скачивание книг с сайта tululu')
    parser.add_argument('start_id', help='Начало диапазона с id книги для скачивания', nargs='?', type=int, default=1)
    parser.add_argument('end_id', help='Конец диапазона с id книги для скачивания', nargs='?', type=int, default=10)
    args = parser.parse_args()

    for book_id in range(args.start_id, args.end_id+1):
        try:
            url = f'https://tululu.org/b{book_id}/'
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            
            book = parse_book_page(response.text, url)
            
            filename = f'{book_id}. {book["title"]}.txt'
            url = 'https://tululu.org/txt.php'
            download_txt(url, filename, book_id)
            
            download_image(book['image_url'], book['image_name'])
        
        except requests.ConnectionError:
            logging.info('Проблема подключения. Повторная попытка через 60 секунд.')
            time.sleep(60)
            continue
        except requests.HTTPError:
            logging.info(f'Страницы {url} нет на сайте.')
