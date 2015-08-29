from django.shortcuts import render_to_response

def index(request):
    return render_to_response('website/index.html')

def product(request):
    return render_to_response('website/product.html')

def signin(request):
    return render_to_response('website/signin.html')

def login(request):
    return render_to_response('website/login.html')
