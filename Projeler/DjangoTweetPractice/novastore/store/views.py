from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "store/index.html")


def product_detail(request):
    return render(request, "store/product_detail.html")
