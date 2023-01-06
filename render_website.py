import json
import math
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    
    with open("books.json", "r") as my_file:
        books_json = my_file.read()
    
    books = json.loads(books_json)
    
    os.makedirs('pages', exist_ok=True)
    
    for page, books_on_page in enumerate(chunked(books, 10), 1):
        count_pages = math.ceil(len(books)/10)
        rendered_page = template.render(books=books_on_page, count_pages=count_pages, current_page=page)
        with open(f'pages/index{page}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.', default_filename='./pages/index1.html')
