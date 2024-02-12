from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas
from auxiliary_functions import get_delta_years, get_word_chape
from collections import defaultdict
import argparse

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()


def main():
    parser = argparse.ArgumentParser(
        description='Скрипт для запуска сайта'
    )
    parser.add_argument('--path', default='wine3.xlsx', type=str, help='input path')
    args = parser.parse_args()

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    years_delta = get_delta_years()
    word_chape = get_word_chape(years_delta)

    column = pandas.read_excel(args.path, sheet_name='Лист1', keep_default_na=False)
    description_drinks = column.to_dict(orient='records')
    categories = sorted(column['Категория'].tolist())
    complete_categories = defaultdict(list, {cat: [wine for wine in description_drinks
                                                   if wine['Категория'] == cat] for cat in categories})

    rendered_page = template.render(
        age=f'{years_delta}',
        word_chape=f'{word_chape}',
        wines=complete_categories
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


if __name__ == '__main__':
    main()