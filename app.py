from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import pandas as pd

app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")


def read_csv_file(file_path):
    return pd.read_csv(file_path)


def create_index():
    if not es.indices.exists(index="quotes1"):
        es.indices.create(index="quotes1")


def index_quotes_from_csv():
    quotes_df = read_csv_file(
        '/Users/aishwarya/Downloads/quotes_funny.csv')  # Update this path
    for id, row in quotes_df.iterrows():
        quote = {
            "author": row['author'],
            "quote": row['quote']
        }
        # print(quote)
        es.index(index='quotes1', id=id, document=quote)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    res = es.search(index="quotes1", body={
                    "query": {"match": {"quote": '*'+query+'*'}}})
    print(res)
    return render_template('result.html', results=res['hits']['hits'])


if __name__ == '__main__':
    create_index()
    index_quotes_from_csv()
    app.run(debug=True)
