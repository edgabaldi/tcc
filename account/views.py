from django.shortcuts import render_to_response
from django.views.generic.list import ListView

from account.models import User

class AccountListView(ListView):
    model = User
    template_name='account/account_list.html'
    paginate_by=50


def customer_form(request):
    return render_to_response('customer/customer_form.html', context = {
        'menu_active':'customer'})
