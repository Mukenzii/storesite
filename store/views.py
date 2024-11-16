from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from .forms import *
from django.contrib import messages

from .models import *
from .utils import *


class ProductList(ListView):
    model = Product
    extra_context = {
        'title': "TOTEMBO: Asosiy sahifa",
    }
    template_name = 'store/index.html'
    context_object_name = 'categories'

    def get_queryset(self):
        categories = Category.objects.filter(parent=None)
        return categories


class ProductListByCategory(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/category_product_list.html'

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        subcategories = category.subcategory.all()
        products = Product.objects.filter(category__in=subcategories)
        sort_field = self.request.GET.get('sort')
        if sort_field:
            products = products.order_by(sort_field)
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = f"Kategoriya: {Category.objects.get(slug=self.kwargs['slug']).title}"
        return context


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = Product.objects.get(slug=self.kwargs['slug']).title
        context['review_form'] = ReviewForm()
        reviews = Review.objects.filter(product__slug=self.kwargs['slug'], publish=True)
        if reviews.count() >= 1:
            context['reviews'] = reviews
        data = []
        products = Product.objects.filter(quantity__gt=0)
        for i in range(4):
            from random import randint
            random_index = randint(0, len(products) - 1)
            data.append(products[random_index])
        context['products'] = data
        return context


def user_login(request):
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('index')
    else:
        messages.error(request, "Noto'g'ri parol yoki login")
        return redirect('login_register')


def user_logout(request):
    logout(request)
    return redirect('index')


def register(request):
    form = RegistrationForm(data=request.POST)
    if form.is_valid():
        user = form.save()
        messages.success(request, "Akkaunt yaratildi!")
    else:
        for error in form.errors:
            messages.error(request, form.errors[error][0])
    return redirect('login_register')


def login_register(request):
    context = {
        'login_form': LoginForm(),
        'registration_form': RegistrationForm(),
        'title': "Ro'yxatdan o'tish yoki kirish"
    }
    return render(request, 'store/login_registration.html', context)

def save_review(request, product_slug):
    form = ReviewForm(data=request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.author = request.user
        product = Product.objects.get(slug=product_slug)
        review.product = product
        review.save()
    else:
        messages.error(request, "Izoh saqlanmadi")
    return redirect('product_detail', product_slug)

def save_or_delete_fav_products(request, product_slug):
    user = request.user if request.user.is_authenticated else None
    product = Product.objects.get(slug=product_slug)

    if user:
        favourite_products = FavouriteProducts.objects.filter(user=user)
        if product in [i.product for i in favourite_products]:
            fav_product = FavouriteProducts.objects.get(user=user, product=product)
            fav_product.delete()
        else:
            FavouriteProducts.objects.create(user=user, product=product)
    next_page = request.META.get('HTTP_REFERER', 'index')
    return redirect(next_page)

class FavouriteProductsView(ListView):
    model = FavouriteProducts
    context_object_name = 'products'
    template_name = 'store/favourite_products.html'

    def get_queryset(self):
        user = self.request.user
        fav = FavouriteProducts.objects.filter(user=user)
        products = [i.product for i in fav]
        return products


def cart(request):

    cart_info = get_cart_data(request)
    context = {
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'order': cart_info['order'],
        'products': cart_info['products'],
    }
    return render(request, 'store/cart.html', context)

def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request, product_id, action)
        return redirect('cart')
    else:
        messages.error(request, "Avtorizatsiyadan o'ting!")
        return redirect('login_registration')

def checkout(request):
    cart_info = get_cart_data(request)
    context = {
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'order': cart_info['order'],
        'products': cart_info['products'],
        'customer_form': CustomerForm(),
        'shipping_form': ShippingForm(),
        'title': "Buyurtma berish"
    }
    return render(request, 'store/checkout.html', context)



