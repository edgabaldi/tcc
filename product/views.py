from django.shortcuts import render_to_response


def product_list(request):
    return render_to_response('product/product_list.html', context = {
        'menu_active': 'product'})

def product_form(request):
    return render_to_response('product/product_form.html', context={
        'menu_active': 'product'})
