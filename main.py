from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas
from auxiliary_functions import get_delta_years, get_word_chape
from collections import defaultdict

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

delta_years = get_delta_years()
word_chape = get_word_chape(delta_years)

column = pandas.read_excel('wine3.xlsx', sheet_name='Лист1')
column_headings = (list(column.columns.ravel()))
excel_data_df = pandas.read_excel('wine3.xlsx', sheet_name='Лист1', usecols=column_headings,
                                  keep_default_na=False)
description_drinks = excel_data_df.to_dict(orient='records')
# categories = sorted(list(dict.fromkeys(excel_data_df['Категория'].tolist())))
categories = sorted(excel_data_df['Категория'].tolist())
complete_categories = defaultdict(list, {cat: [wine for wine in description_drinks
                                               if wine['Категория'] == cat] for cat in categories})

rendered_page = template.render(
    age=f'{delta_years}',
    word_chape=f'{word_chape}',
    wines=complete_categories
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)


server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()