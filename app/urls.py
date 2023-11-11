from django.urls import path, include
from app import views

urlpatterns = [
    # Pages
    path("", views.index_view, name="index"),
    path("product-details/", views.product_details, name="product_details"),
    path("recommendation-details/", views.recommendation_view, name="recommendation_product"),


    # Auth
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

]
