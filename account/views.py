#coding:utf-8
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy

from account.models import User
from account import forms
from core.views import SearchableListView


class UserListView(SearchableListView):
    """
    View that list users and filter
    """

    model = User
    template_name='account/user_list.html'
    paginate_by=25
    form_class=forms.UserSearchForm
    queryset = User.objects.all().order_by('is_active')


class UserActionMixin(object):
    """
    Common attributes for user actions
    """

    model = User
    form_class = forms.UserModelForm 
    template_name = 'account/user_form.html'
    success_url = reverse_lazy('user_list')


class BaseUserActionMixin(UserActionMixin, SuccessMessageMixin):
    """
    Mixin of UserActionMixin with success messages
    """
    success_message = 'Usuário salvo com sucesso.'

class UserCreateView(BaseUserActionMixin, CreateView):
    """
    View that allow create an user
    """


class UserUpdateView(BaseUserActionMixin, UpdateView):
    """
    User that allow update an user
    """


class ActivateUserView(BaseUserActionMixin, UpdateView):
    """
    View that allow activate/deactivate user in system.
    """

    form_class=forms.ActivateUserModelForm
    template_name = 'account/user_activate.html'
    success_message = 'Ativação/Rejeição de usuário salva!'

    def form_valid(self, form):

        is_activated = form.cleaned_data.get('is_active')

        if is_activated:
            form.send_email_activate(self.object)
        else:
            form.send_email_deactivate(self.object)

        return super(ActivateUserView, self).form_valid(form)
