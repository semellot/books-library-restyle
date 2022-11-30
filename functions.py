import os
from os.path import basename
from urllib.parse import urljoin, urlsplit, unquote

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import requests


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError()


def download_txt(url, filename, book_id, folder='books/'):
    params = {
        'id': book_id
    }
    response = requests.get(url, params=params, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)
    
    os.makedirs(folder, exist_ok=True)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w') as file:
        file.write(response.text)
    
    return filename


def download_image(url, filename, folder='images/'):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)
    
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    
    return filename


def parse_book_page(book_page, url):
    soup = BeautifulSoup(book_page, 'lxml')
    title_tag = soup.find('div', id='content').find('h1')
    title_full = title_tag.text
    title, author = title_full.split('::')
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
        'author': author.strip(),
        'image_src': f'images/{image_name}',
        'image_url': image_url,
        'image_name': image_name,
        'comments': comments,
        'genres': genres
    }
    
    return book