from django.urls import path, include
from api import views

urlpatterns = [
    path("get-product/<str:category>/", views.get_product, name="get_product"),
    path("get-product/", views.get_product, name="get_all_products"),
    path("get-product-random/", views.get_product_random, name="get_all_products_random"),
    path("get-product-recommendation/", views.get_recommendation_data, name="get_recommendation_data"),

    
]