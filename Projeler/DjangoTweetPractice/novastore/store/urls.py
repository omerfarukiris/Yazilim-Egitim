from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("", views.index, name="index"),
    path("urun/", views.product_detail, name="product_detail"),
]
