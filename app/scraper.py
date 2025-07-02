import os
import json
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from app.utils import extract, selectors
from config import headers

class CeneoScraper:
    def __init__(self, product_id):
        self.product_id = product_id
        self.product_name = ""
        self.opinions = []
        self.product_info = {}

    def fetch_product(self):
        url = f"https://www.ceneo.pl/{self.product_id}#tab=reviews"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return False
        page_dom = BeautifulSoup(response.text, 'html.parser')
        self.product_name = extract(page_dom, 'h1')
        opinions_count = extract(page_dom, 'a.product-review__link > span')
        if not opinions_count:
            return False
        self.product_info["opinions_count"] = opinions_count
        return True

    def scrape_all_opinions(self):
        url = f"https://www.ceneo.pl/{self.product_id}#tab=reviews"
        while url:
            response = requests.get(url, headers=headers)
            page_dom = BeautifulSoup(response.text, 'html.parser')
            for opinion in page_dom.select('div.js_product-review:not(.user-post--highlight)'):
                self.opinions.append({key: extract(opinion, *value) for key, value in selectors.items()})
            next_url = extract(page_dom, 'a.pagination__next', 'href')
            url = "https://www.ceneo.pl" + next_url if next_url else None

    def save_data(self):
        opinions_path = f"./app/data/opinions/{self.product_id}.json"
        os.makedirs(os.path.dirname(opinions_path), exist_ok=True)
        with open(opinions_path, "w", encoding="UTF-8") as f:
            json.dump(self.opinions, f, indent=4, ensure_ascii=False)

        df = pd.DataFrame.from_dict(self.opinions)
        df["stars"] = df["stars"].apply(lambda s: float(s.split("/")[0].replace(',', '.'))).astype(float)
        pros_count = int(df["pros"].astype(bool).sum())
        cons_count = int(df["cons"].astype(bool).sum())

        self.product_info.update({
            "product_id": self.product_id,
            "product_name": self.product_name,
            "pros_count": pros_count,
            "cons_count": cons_count,
            "average_stars": float(df["stars"].mean()),
            "stars_distr": df["stars"].value_counts().reindex(np.arange(0, 5.5, 0.5), fill_value=0).to_dict(),
            "recommendation_distr": df["recommendation"].value_counts(dropna=False).reindex(["Nie polecan", "Polecam", None], fill_value=0).to_dict()
        })

        products_path = f"./app/data/products/{self.product_id}.json"
        os.makedirs(os.path.dirname(products_path), exist_ok=True)
        with open(products_path, "w", encoding="UTF-8") as f:
            json.dump(self.product_info, f, indent=4, ensure_ascii=False)