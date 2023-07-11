from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender

# Create your views here.
def product_list(request, product_category_slug=None):
    category = None
    categories = ProductCategory.objects.all()
    products = Product.objects.filter(available=True)
    
    if product_category_slug:
        category = get_object_or_404(ProductCategory, slug=product_category_slug)
        products = products.filter(category=category)
        
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                    'products': products})
    

def product_detail(request, id, slug):
    product = get_object_or_404(Product, 
                                id=id, 
                                slug=slug, 
                                available=True)
    cart_product_form = CartAddProductForm()
    
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'recommended_products': recommended_products})
    
        
        