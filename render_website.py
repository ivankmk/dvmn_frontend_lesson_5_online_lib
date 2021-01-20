from livereload import Server, shell
import json
from more_itertools import chunked
import math
from jinja2 import Environment, FileSystemLoader, select_autoescape


def rebuild():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open("books_db.json", "r") as my_file:
        books_json = my_file.read()

    all_books = json.loads(books_json)

    for i, book_chunk in enumerate(chunked(all_books, 10)):
    
        col1, col2 = list(
            chunked(book_chunk, math.ceil(len(book_chunk)/2))
            )

        rendered_page = template.render(col1=col1, col2=col2)

        with open(f'pages/index{i}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)

    print("Site rebuilded")


rebuild()

server = Server()

server.watch('template.html', rebuild)

server.serve(root='.')