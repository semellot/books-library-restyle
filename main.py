import os
import requests


def check_for_redirect(response):
    if response.status_code == 302:
        raise requests.HTTPError()


url = "https://tululu.org/txt.php"

book_id = 1

while book_id <= 10:
    try:
        params = {
            "id": book_id
        }
        response = requests.get(url, params=params, allow_redirects=False)
        response.raise_for_status() 
        check_for_redirect(response)
        
        os.makedirs("books", exist_ok=True)
        filename = f'books/id{book_id}.txt'
        with open(filename, 'w') as file:
            file.write(response.text)
        
    except requests.HTTPError:
        pass
    
    book_id += 1
