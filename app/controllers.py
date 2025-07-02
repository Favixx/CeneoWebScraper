from flask import Blueprint, render_template, request, redirect, url_for
from app.scraper import CeneoScraper
from app.models import Product
import os
import json
import pandas as pd

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/extract", methods=["GET"])
def display_form():
    return render_template("extract.html")

@main.route("/extract", methods=["POST"])
def extract_data():
    product_id = request.form.get("product_id")
    scraper = CeneoScraper(product_id)
    if not scraper.fetch_product():
        return render_template("extract.html", error="Nie znaleziono opinii lub błędne ID.")
    
    scraper.scrape_all_opinions()
    scraper.save_data()

    return redirect(url_for("main.product", product_id=product_id))

@main.route("/products")
def products():
    try:
        return render_template("products.html", products=Product.get_all())
    except FileNotFoundError:
        return render_template("products.html", error="Nie pobrano jeszcze żadnch danych")

@main.route("/author")
def author():
    return render_template("author.html")

@main.route("/product/<product_id>")
def product(product_id):
    try:
        opinions = Product.load_opinions(product_id)
        df = pd.DataFrame(opinions)
        df["pros"] = df["pros"].apply(Product.list_to_text)
        df["cons"] = df["cons"].apply(Product.list_to_text)
        return render_template("product.html", opinions=df.to_html(classes="table table-hover table-bordered table-striped", index=False), product_id=product_id)
    except Exception as e:
        return render_template("product.html", error=str(e))

@main.route("/download/<product_id>/<file_format>")
def download(product_id, file_format):
    return Product.download_file(product_id, file_format)
