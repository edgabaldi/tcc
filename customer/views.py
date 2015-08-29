from django.shortcuts import render_to_response

def customer_list(request):
    return render_to_response('customer/customer_list.html')
