from livereload import Server, shell
import json

from jinja2 import Environment, FileSystemLoader, select_autoescape


def rebuild():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open("books_db.json", "r") as my_file:
        books_json = my_file.read()

    books = json.loads(books_json)

    rendered_page = template.render(books=books)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    print("Site rebuilded")


rebuild()

server = Server()

server.watch('template.html', rebuild)

server.serve(root='.')