import argparse
import os
from os.path import basename
from urllib.parse import urljoin, urlsplit, unquote

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import requests


def check_for_redirect(response):
    for resp in response.history:
        raise requests.HTTPError()


def download_txt(url, filename, folder='books/'):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)
    
    os.makedirs(folder, exist_ok=True)
    filename = sanitize_filename(filename)
    filename = os.path.join(folder, filename)
    with open(filename, 'w') as file:
        file.write(response.text)
    
    return filename


def download_image(url, filename, folder='images/'):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)
    
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, filename)
    with open(filename, 'wb') as file:
        file.write(response.content)
    
    return filename


def parse_book_page(book_page, url):
    soup = BeautifulSoup(book_page, 'lxml')
    title_tag = soup.find('div', id='content').find('h1')
    title_full = title_tag.text
    title, author = title_full.split("::")
    title = title.strip()
    
    image_short_url = soup.find('div', class_='bookimage').find('img')['src']
    image_url = urljoin(url, image_short_url)
    image_name = unquote(basename(urlsplit(image_url)[2]))
    
    comments = soup.find_all('div', class_='texts')
    comments = [comment.find('span').text for comment in comments]
    
    genres = soup.find('span', class_='d_book').find_all('a')
    genres = [genre.text for genre in genres]
    
    book = {
        'title': title,
        'image_url': image_url,
        'image_name': image_name,
        'comments': comments,
        'genres': genres
    }
    
    return book


if __name__ == "__main__":
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
            url = f'https://tululu.org/txt.php?id={book_id}'
            download_txt(url, filename)
            
            download_image(book['image_url'], book['image_name'])

        except requests.HTTPError:
            pass
