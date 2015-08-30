from django.shortcuts import render_to_response


def product_list(request):
    return render_to_response('product/product_list.html')

def product_form(request):
    return render_to_response('product/product_form.html')
