import os
from os.path import basename
from urllib.parse import urljoin, urlsplit, unquote

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import requests


def check_for_redirect(response):
    # print("response.status_code:", response.status_code)
    if response.status_code == 302:
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
    # filename = sanitize_filename(filename)
    filename = os.path.join(folder, filename)
    with open(filename, 'wb') as file:
        file.write(response.content)
    
    return filename


book_id = 1

while book_id <= 10:
    try:
        print('book', book_id)
        url = f'https://tululu.org/b{book_id}/'
        response = requests.get(url, allow_redirects=False)
        response.raise_for_status()
        check_for_redirect(response)
        
        soup = BeautifulSoup(response.text, 'lxml')
        title_tag = soup.find('div', id='content').find('h1')
        title_full = title_tag.text
        title, author = title_full.split("::")
        title = title.strip()
        filename = f'{book_id}. {title}.txt'
        url = f'https://tululu.org/txt.php?id={book_id}'
        # download_txt(url, filename)
        
        image_short_url = soup.find('div', class_='bookimage').find('img')['src']
        image_url = urljoin('https://tululu.org', image_short_url)
        image_name = unquote(basename(urlsplit(image_url)[2]))
        download_image(image_url, image_name)
        
        comments = soup.find_all('div', class_='texts')
        for comment in comments:
            comment_text = comment.find('span').text
            print(comment_text)

    except requests.HTTPError:
        pass

    book_id += 1
