from django.urls import path
from . import views

app_name = 'Shop_App'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    # path('categories/', views.category_list_view, name='category_list'),
    # path('categories/<int:pk>/', views.category_product_view, name='category_products'),
    path('categories/', views.Categories.as_view(), name='category_list'),
    path('category-wise-products/<pk>', views.CategoryWiseProducts.as_view(), name='category_wise_product_list'),
    path('product/<pk>', views.ProductDetail.as_view(), name='product_detail'),
    path('search/', views.search_products, name='search_products'),
    path('product-suggestions/', views.product_suggestions, name='product_suggestions'),
    path('products-from-search/', views.product_list, name='product_list'),
    path('products-from-using_seemore/', views.product_list, name='load_more_products'),

]
