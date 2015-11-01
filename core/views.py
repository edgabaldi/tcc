#coding:utf-8
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages


class SearchableListView(FormMixin, ListView):

    http_method_names = ['get']

    def get_form_kwargs(self):

        return {
            'initial': self.get_initial(), 
            'data': self.request.GET,
        }

    def get(self, request, *args, **kwargs):

        self.form = self.get_form(self.get_form_class())

        if self.form.is_valid():
            self.object_list = self.form.get_result_queryset()
        else:
            self.object_list = self.get_queryset()

        context = self.get_context_data(
            object_list = self.object_list,
            form = self.form
        )

        return self.render_to_response(context)


class LoginRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated():
            messages.warning(request, u'Você precisa estar autenticado para acessar essa página')
            return HttpResponseRedirect(reverse_lazy('login'))
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
