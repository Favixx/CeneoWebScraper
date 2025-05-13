import os
import json
from app import app
from flask import render_template, abort

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    return render_template('extract.html')

@app.route('/products')
def products():
    products_dir = 'app/data/products'
    products_list = []

    for filename in os.listdir(products_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(products_dir, filename)
            with open(filepath, 'r', encoding="utf-8") as f:
                try:
                    product = json.load(f)
                    products_list.append(product)
                except json.JSONDecodeError:
                    continue

    return render_template('products.html', products=products_list)

@app.route('/author')
def author():
    return render_template('author.html')

@app.route('/products/<int:product_id>')
def product(product_id):
    filepath = f'app/data/products/{product_id}.json'
    
    if not os.path.exists(filepath):
        abort(404)

    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            product_data = json.load(f)
        except json.JSONDecodeError:
            abort(500)

    return render_template('product.html', product=product_data)