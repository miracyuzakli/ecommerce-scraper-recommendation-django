from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import json
import pandas as pd



def getProductInformation(url: str, category: str, product_id: int, image_path: str = "") -> dict:
    # Selenium tarayıcısını başlat
    driver = webdriver.Chrome()

    # Ürün sayfasını aç
    driver.get(url)
    product_classes = {
        "product": "pr-new-br",                             # Ürün başlığı
        "price": "prc-dsc",                                 # Fiyat
        "rating": "total-review-count",                     # Değerlendirme
        "rating_score": "rating-line-count",                # Değerlendirme skoru
        "answered_questions": "answered-questions-count",   # Soru-Cevap
        "favorite": "product-favorite-info",                # Favori eklenme sayısı
    }

    product_dict = {
        "category": category
    } # Mevcur ürün hakkında ki bilgilerin tutulacağı dict


    for i in product_classes:
        try:
            product_dict[i] = driver.find_element(By.CLASS_NAME, product_classes[i]).text
        except:
            product_dict[i] = None
            print(f"Block 1: feature_{i} - Error !\nURL : {url}\n")

    # Ürün bilgileri
    product_information = driver.find_elements(By.CLASS_NAME, "attribute-item")
    for i, item in enumerate(product_information):
        try:
            label = item.find_element(By.CLASS_NAME, "attribute-label")
            value = item.find_element(By.CLASS_NAME, "attribute-value")
            product_dict[f"feature_{i}"] = f"{label.text} | {value.text}"
        except:
            product_dict[f"feature_{i}"] = None
            print(f"Block 2: feature_{i} -  Error !\nURL : {url}\n")


    # Görsel indirme işlemleri
    try:
        image_cont = driver.find_element(By.CLASS_NAME, 'base-product-image')
        product_image = image_cont.find_element(By.TAG_NAME, 'img')
        image_url = product_image.get_attribute('src')

        response = requests.get(image_url)
        if response.status_code == 200:
            with open(f"{image_path}\{category}_image_{product_id}.png", "wb") as f:
                f.write(response.content)
        else:
            print("Görsel indirme işlemi başarısız.")
        product_dict["image_name"] = f"{category}_image_{product_id}.png"
    except:
        product_dict["image_name"] = "default_image.png"
        print(f"Block 2: Error !\nURL : {url}\n")


    
    driver.quit() # Tarayıcıyı kapat


    return product_dict

if __name__ == "__main__":
    
    with open('product_urls_data.json', 'r') as dosya:
        json_data = json.load(dosya)

    url_list = list()
    data_list = list()
    product_id = 0
    for data in json_data:
        url = data["url"]
        category = data["category"]

        if url not in url_list:

            url_list.append(url)
            data_list.append(getProductInformation(url, category, product_id, "images"))
            product_id += 1

        print(f"------ {product_id} ------------- Tamamlandı...")
       

    df = pd.DataFrame(data_list)
    print(df)
    df.to_csv("data.csv", index=False)



