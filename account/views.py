from django.shortcuts import render_to_response

def customer_list(request):
    return render_to_response('customer/customer_list.html', context = {
        'menu_active':'customer'})

def customer_form(request):
    return render_to_response('customer/customer_form.html', context = {
        'menu_active':'customer'})
