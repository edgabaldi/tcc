from django.views.generic.edit import CreateView, UpdateView

from account.models import User
from account.forms import UserModelForm, UserSearchForm
from core.views import SearchableListView


class UserListView(SearchableListView):
    """
    View that list users and filter
    """

    model = User
    template_name='account/user_list.html'
    paginate_by=25
    form_class=UserSearchForm


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
