import argparse
import json
import math
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


COUNT_BOOKS_ON_PAGE = 10

def on_reload():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_path', help='Путь к json', nargs='?', default='books.json')
    args = parser.parse_args()
    
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    
    with open(args.json_path, 'r') as my_file:
        books_json = my_file.read()
    
    books_descriptions = json.loads(books_json)
    
    os.makedirs('pages', exist_ok=True)
    
    count_pages = math.ceil(len(books_descriptions)/COUNT_BOOKS_ON_PAGE)
    for page, books_on_page in enumerate(chunked(books_descriptions, COUNT_BOOKS_ON_PAGE), 1):
        rendered_page = template.render(books=books_on_page, count_pages=count_pages, current_page=page)
        with open(f'pages/index{page}.html', 'w', encoding='utf8') as file:
            file.write(rendered_page)

def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', default_filename='./pages/index1.html')


if __name__ == '__main__':
    main()
