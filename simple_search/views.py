from django.shortcuts import render

class SearchFormListView(FormMixin, ListView):
    """
    ListView with search filter form
    """
    http_method_names = ['get']

    def get_form_kwargs(self):
        return {'initial': self.get_initial(), 'data': self.request.GET}

    def get(self, request, *args, **kwargs):

        self.form = self.get_form(self.get_form_class())

        if self.form.is_valid():
            self.object_list = self.form.get_result_queryset()
        else:
            self.object_list = self.get_queryset()

        context = self.get_context_data(
            object_list=self.object_list,
            form=self.form,
            url_params=request.GET.urlencode()
        )

        return self.render_to_response(context)
