from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from account.models import User
from account.forms import UserModelForm


class UserListView(ListView):
    """
    View that list users
    """

    model = User
    template_name='account/user_list.html'
    paginate_by=25


class UserActionMixin(object):
    """
    Common attributes for user actions
    """

    model = User
    form_class = UserModelForm 
    template_name = 'account/user_form.html'


class UserCreateView(UserActionMixin, CreateView):
    """
    View that allow create an user
    """


class UserUpdateView(UserActionMixin, UpdateView):
    """
    User that allow update an user
    """
