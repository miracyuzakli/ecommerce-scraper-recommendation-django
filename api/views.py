from django.shortcuts import render

# Create your views here.
from .models import Product, UserProductViewing

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from random import sample

import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from keras.models import load_model

import json

def get_product(request, category=None):
    if category is not None:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()  # Tüm ürünleri almak için `filter` yerine `all()` kullanıyoruz.

 

    product_list = []
    for product in products:
        product_dict = {
            'id': product.id,
            'category': product.category,
            'product_name': product.product_name,
            'price': product.price,
            'rating': product.rating,
            'rating_score': product.rating_score,
            'answered_questions': product.answered_questions,
            'favorite': product.favorite,
            'feature_0': product.feature_0,
            'feature_1': product.feature_1,
            'feature_2': product.feature_2,
            'feature_3': product.feature_3,
            'feature_4': product.feature_4,
            'feature_5': product.feature_5,
            'feature_6': product.feature_6,
            'feature_7': product.feature_7,
            'image_name': product.image_name,
        }
        product_list.append(product_dict)
    
    return JsonResponse({'products': product_list})




def get_product_random(request):
    categories = ['laptop', 'monitor', 'phone', 'smart-watch', 'television', 'digital-camera']

    product_list = list()

    for category in categories:
        products = Product.objects.filter(category=category)
        # Kategoriden yalnızca 4 ürün al
        products = sample(list(products), 4)

        for product in products:
            product_dict = {
                'id': product.id,
                'category': product.category,
                'product_name': product.product_name,
                'price': product.price if product.price is not None else None,
                'rating': product.rating,
                'rating_score': product.rating_score if product.rating_score is not None else None,
                'answered_questions': product.answered_questions,
                'favorite': product.favorite,
                'feature_0': product.feature_0,
                'feature_1': product.feature_1,
                'feature_2': product.feature_2,
                'feature_3': product.feature_3,
                'feature_4': product.feature_4,
                'feature_5': product.feature_5,
                'feature_6': product.feature_6,
                'feature_7': product.feature_7,
                'image_name': product.image_name,
            }
            product_list.append(product_dict)

    return JsonResponse({'products': product_list})






def get_recommendation_system_value(df, chosen_products):

    df.fillna('', inplace=True)

    # Ürün özelliklerini birleştir
    df['features'] = df['category'].astype(str) + ' ' + df['product_name'] + ' ' + df['feature_0'] + ' ' + df['feature_1'] + ' ' + df['feature_2'] + ' ' + df['feature_3'] + ' ' + df['feature_4'] + ' ' + df['feature_5'] + ' ' + df['feature_6'] + ' ' + df['feature_7']

    # TF-IDF vektörleme
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['features'])

    # Modeli yükle
    model = load_model('ML/recommendation_system.h5')

    # Cosine Similarity ile benzerlik matrisini hesapla
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

   

    # Seçilen ürünlere benzer ürünlerin indexlerini ve benzerlik skorlarını al
    similar_products = []
    for product in chosen_products:
        product_index = df[df['product_name'] == product.strip()].index[0]
        similar_products += list(enumerate(cosine_sim[product_index]))

    # Benzerlik skorlarına göre ürünleri sırala
    sorted_similar_products = sorted(similar_products, key=lambda x:x[1], reverse=True)

    # En benzer 5 ürünü yazdır (seçilen ürünleri hariç)
    count = 0
    data_dict = list()
    for i in range(len(sorted_similar_products)):
        if df['product_name'][sorted_similar_products[i][0]] not in chosen_products:
            # print(df['product'][sorted_similar_products[i][0]])
            current_column = df.iloc[[sorted_similar_products[i][0]],:]

            temp_dict = {
                "model_score": sorted_similar_products[i][0]
            }
            
            for j in df.columns.values:

                temp_dict[j] = str(current_column[j].values[0])
            
            data_dict.append(temp_dict)

    
            count += 1
            if count == 12:
                break


    return data_dict



def get_recommendation_data(request):

    all_products = Product.objects.all()

    data = list(all_products.values())
    df = pd.DataFrame(data)


    user_product_viewing = UserProductViewing.objects.filter(user=request.user.id)
    chosen_products = list()
    for product in user_product_viewing:
        if df["product_name"][product.product_id] not in chosen_products:
            chosen_products.append(df["product_name"][product.product_id])
 
    print("#"*100)
    print(chosen_products)
    recommendation_data = get_recommendation_system_value(df, chosen_products)
   


    return JsonResponse({'recommendation_data': recommendation_data})
