from core.views import SearchableListView
from product.models import Product
from product.forms import ProductSearchForm


class ProductSearchableListView(SearchableListView):
    """
    View that allow list and search products
    """
    model = Product
    template_name = 'product/product_list.html'
    paginate_by=25
    form_class = ProductSearchForm


def product_form(request):
    return render_to_response('product/product_form.html', context={
        'menu_active': 'product'})
