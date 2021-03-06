from livereload import Server
import json
from more_itertools import chunked
import math
import re
import os
import glob
from jinja2 import Environment, FileSystemLoader, select_autoescape


def remove_old_pages(remove_after):
    for page in glob.glob('pages/index*.html'):
        page_number = int(re.search(r'\d+', page).group(0))
        if page_number > remove_after:
            os.remove(page)
            print(f'Page {page} was removed.')


def rebuild():

    elements_on_page = 10

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open("books_db.json", "r") as my_file:
        books_json = my_file.read()

    all_books = list(chunked(json.loads(books_json), elements_on_page))

    pages = len(all_books)

    remove_old_pages(pages)

    for page_num, book_chunk in enumerate(all_books, 1):
        books = list(chunked(book_chunk, math.ceil(len(book_chunk)/2)))

        rendered_page = template.render(
            books=books,
            page_num=page_num,
            pages=pages
            )

        with open(f'pages/index{page_num}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)

    print("Site rebuilded")


if __name__ == '__main__':
    rebuild()
    server = Server()
    server.watch('template.html', rebuild)
    server.serve(root='.')
