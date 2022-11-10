import os
import requests

url = "https://tululu.org/txt.php"

book_id = 1

while book_id <= 10:
    params = {
        "id": book_id
    }
    response = requests.get(url, params=params)
    response.raise_for_status() 
    
    os.makedirs("books", exist_ok=True)
    filename = f'books/id{book_id}.txt'
    with open(filename, 'w') as file:
        file.write(response.text)
    book_id += 1
    
    