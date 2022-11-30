from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


if __name__ == "__main__":
    url = 'https://tululu.org/l55/'
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    books = soup.find_all('div', class_='bookimage')
    for book in books:
        book_href = book.find('a')['href']
        book_url = urljoin('https://tululu.org', book_href)
        print(book_url)
