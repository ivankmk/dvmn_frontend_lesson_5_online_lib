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

    all_books = list(chunked(json.loads(books_json), 10))

    pages = len(list(all_books))

    for page_num, book_chunk in enumerate(all_books, 1):
        col1, col2 = list(
            chunked(book_chunk, math.ceil(len(book_chunk)/2))
            )

        rendered_page = template.render(
            col1=col1,
            col2=col2,
            page_num=page_num,
            pages=pages
            )

        with open(f'index{"" if page_num == 1 else page_num}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)

    print("Site rebuilded")


rebuild()

server = Server()

server.watch('template.html', rebuild)

server.serve(root='.')