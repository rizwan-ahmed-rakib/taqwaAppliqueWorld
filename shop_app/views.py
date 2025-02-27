from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse

# Create your views here for your models
from shop_app.models import Product, Category
from promotion_app.models import VideoPromotion
# mixin
from django.contrib.auth.mixins import LoginRequiredMixin

"""classbase view"""


class Home(ListView):
    model = Product
    template_name = 'shop_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Category মডেলের সব অবজেক্ট পাঠানো হলো
        context['vid'] = VideoPromotion.objects.all()  # Category মডেলের সব অবজেক্ট পাঠানো হলো
        return context


class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'shop_app/product_detail.html'


def search_products(request):
    query = request.GET.get('q', '')  # Search query GET parameter theke anchi
    products = Product.objects.filter(name__icontains=query)  # Name field e search
    return render(request, 'shop_app/search_results.html', {'products': products, 'query': query})


def product_suggestions(request):
    query = request.GET.get('term', '')  # User input paoa
    products = Product.objects.filter(name__icontains=query)[:10]  # 10 ta suggestion
    suggestions = list(products.values('id', 'name'))  # ID ebong name return korbo
    return JsonResponse(suggestions, safe=False)  # JSON format e data pathano


class Categories(ListView):
    model = Category
    template_name = 'shop_app/category.html'
    context_object_name = 'categories'


class CategoryWiseProducts(ListView):
    model = Product
    template_name = 'shop_app/categorywiseProduct.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # URL থেকে category_id নিচ্ছি
        category_id = self.kwargs.get('pk')
        category = get_object_or_404(Category, pk=category_id)

        # প্রাসঙ্গিক ক্যাটাগরির প্রোডাক্ট ফিল্টার
        context['category'] = category
        context['products'] = Product.objects.filter(category=category)

        return context


def product_list(request):
    query = request.GET.get('query', '')  # Search query
    sort_by = request.GET.get('sort_by', 'name')  # Sorting field
    category = request.GET.get('category', '')  # Filter by category

    # Fetch all products
    products = Product.objects.all()

    # Filter by search query
    if query:
        products = products.filter(name__icontains=query)

    # Filter by category if provided
    if category:
        products = products.filter(category__id=category)  # Use category's ID for filtering

    # Sort the products
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('name')  # Default sorting by name

    # Fetch all categories for the filter
    categories = Category.objects.all()  # Get all categories

    context = {
        'products': products,
        'query': query,
        'sort_by': sort_by,
        'category': category,
        'categories': categories,  # Pass categories to template
    }

    return render(request, 'shop_app/product_list.html', context)


def load_more_products(request):
    start = int(request.GET.get('start', 0))
    products = Product.objects.all()[start:start + 10]
    data = {
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "old_price": p.old_price,
                "image": p.mainimage.url
            } for p in products
        ],
        "hasMore": Product.objects.count() > start + 10
    }
    return JsonResponse(data)
