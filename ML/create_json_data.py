import pandas as pd
import json


json_list = list()

data = pd.read_csv("data.csv")

for i in data.index.values:
    current_row = data.iloc[i, :]
    
    temp = {
    "model": "api.product",
    "pk": int(i+1),
    "fields": {
      "category": current_row["category"],
      "product_name": current_row["product"],
      "price": float(current_row["price"]),
      "rating": float(current_row["raiting"]),
      "rating_score": float(current_row["raiting_score"]),
      "answered_questions": float(current_row["answered_questions"]),
      "favorite": float(current_row["favorite"]),
      "feature_0": current_row["feature_0"],
      "feature_1": current_row["feature_1"],
      "feature_2": current_row["feature_2"],
      "feature_3": current_row["feature_3"],
      "feature_4": current_row["feature_4"],
      "feature_5": current_row["feature_5"],
      "feature_6": current_row["feature_6"],
      "feature_7": current_row["feature_7"],
      "image_name": current_row["image_name"]
    }
  }

    json_list.append(temp)

with open("products_data.json", "w", encoding="utf-8") as outfile:
    json.dump(json_list, outfile, ensure_ascii=False)