from django.shortcuts import render_to_response
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from account.models import User
from account.forms import UserModelForm 


class UserListView(ListView):
    model = User
    template_name='account/user_list.html'
    paginate_by=50


class UserCreateView(CreateView):
    model = User
    form_class = UserModelForm 
    template_name='account/user_form.html'
