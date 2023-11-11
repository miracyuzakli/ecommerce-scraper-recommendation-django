import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
# Selenium tarayıcısını başlat
driver = webdriver.Chrome()

urls = [
    {"url": "https://www.trendyol.com/laptop-x-c103108?pi=4", "category": "laptop"},
    {"url": "https://www.trendyol.com/cep-telefonu-x-c103498", "category": "phone"},
    {"url": "https://www.trendyol.com/monitor-x-c103668", "category": "monitor"},
    {"url": "https://www.trendyol.com/televizyon-x-c104156", "category": "television"},
    {"url": "https://www.trendyol.com/akilli-saat-x-c1240?pi=6", "category": "smart-watch"},
    {"url": "https://www.trendyol.com/dijital-fotograf-makineleri-x-c104042", "category": "digital-camera"},

    
]



index = 1

data_urls = list()

for url_dict in urls:
    url = url_dict["url"]
    category = url_dict["category"]

    print(f"{category} -- Started ----------------------------------")

    driver.get(url)
    product_data = list()

    while len(product_data) < 1000:
        try:
            products = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "p-card-chldrn-cntnr.card-border")
                )
            )

            # Her bir ürünün URL'sini ve indeksini alın
            for product in products:
                try:
                    product_link = product.find_element(By.TAG_NAME, "a").get_attribute(
                        "href"
                    )
                    product_data.append(
                        {"index": index, "url": product_link, "category": category}
                    )
                    index += 1
                except StaleElementReferenceException:
                    continue

            # Sayfayı aşağı kaydırın
            for _ in range(3):
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.SPACE)
            time.sleep(2)  # 2 saniye bekleme ekledim            time.sleep(10)
        except:
            break

    data_urls += product_data
    print(f"{category} -- Finish ------- Total {len(product_data)} values ---")


with open("product_urls_data.json", "w") as json_file:
    json.dump(data_urls, json_file)

# Tarayıcıyı kapat
driver.quit()
