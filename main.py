import os

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import requests


def check_for_redirect(response):
    print("response.status_code:", response.status_code)
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


book_id = 1

while book_id <= 10:
    try:
        print("book", book_id)
        url = f'https://tululu.org/read{book_id}/'
        response = requests.get(url, allow_redirects=False)
        response.raise_for_status()
        check_for_redirect(response)
        
        soup = BeautifulSoup(response.text, 'lxml')
        title_tag = soup.find('div', id="content").find('h1')
        title_full = title_tag.text
        title, author = title_full.split("::")
        title = title.strip()
        
        filename = f'{book_id}. {title}.txt'
        
        url = f'https://tululu.org/txt.php?id={book_id}'
        download_txt(url, filename)

    except requests.HTTPError:
        pass

    book_id += 1
