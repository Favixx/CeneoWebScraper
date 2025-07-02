import os
import json
import pandas as pd
from flask import current_app, send_file

class Product:
    @staticmethod
    def list_to_text(lst):
        return " • " + ", ".join(lst) if lst else ""

    @staticmethod
    def get_all():
        path = "./app/data/products"
        return [
            json.load(open(os.path.join(path, fname), "r", encoding="utf-8"))
            for fname in os.listdir(path)
            if fname.endswith(".json")
        ]

    @staticmethod
    def load_opinions(product_id):
        path = f"./app/data/opinions/{product_id}.json"
        if not os.path.exists(path):
            raise FileNotFoundError("Nie znaleziono danych dla produktu.")
        return json.load(open(path, "r", encoding="utf-8"))

    @staticmethod
    def download_file(product_id, file_format):
        base_dir = os.path.join(current_app.root_path, "data", "opinions")
        os.makedirs(base_dir, exist_ok=True)

        json_path = os.path.join(base_dir, f"{product_id}.json")
        if not os.path.exists(json_path):
            return f"Nie znaleziono danych dla produktu {product_id}", 404

        df = pd.read_json(json_path)

        match file_format:
            case "json":
                return send_file(json_path, as_attachment=True, download_name=f"{product_id}.json", mimetype="application/json")
            case "csv":
                csv_path = os.path.join(base_dir, f"{product_id}.csv")
                df.to_csv(csv_path, index=False)
                return send_file(csv_path, as_attachment=True, download_name=f"{product_id}.csv", mimetype="text/csv")
            case "xlsx":
                xlsx_path = os.path.join(base_dir, f"{product_id}.xlsx")
                df.to_excel(xlsx_path, index=False)
                return send_file(xlsx_path, as_attachment=True, download_name=f"{product_id}.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            case _:
                return "Nieobsługiwany format pliku", 400
