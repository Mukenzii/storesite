from django.urls import path

from .views import *

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('category/<slug:slug>/', ProductListByCategory.as_view(), name='category_list'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('login_registration/', login_register, name='login_register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('save_review/<slug:product_slug>/', save_review, name='save_review'),
    path('save_or_delete_favourite/<slug:product_slug>/', save_or_delete_fav_products, name='save_or_delete'),
    path('favourite_products/', FavouriteProductsView.as_view(), name='favourite_products'),
    path('cart/', cart, name='cart'),
    path('to_cart/<int:product_id>/<str:action>/', to_cart, name='to_cart'),
    path('checkout/', checkout, name='checkout')
]

