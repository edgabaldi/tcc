from django.test import TestCase
from django.test.client import RequestFactory

from core.tests.test_form_base_search_form import ProductSearchForm
from core.views import SearchableListView

class ProductSearchableListView(SearchableListView):

    form_class = ProductSearchForm


class SearchableListViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.view = ProductSearchableListView

    def test_get(self):
        response = self.view.as_view()(self.request)
        self.assertEqual(response.status_code, 200)
