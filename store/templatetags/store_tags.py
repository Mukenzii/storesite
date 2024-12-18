from django import template
from ..models import Category, FavouriteProducts

register = template.Library()


@register.simple_tag()
def get_all_categories():
    categories = Category.objects.filter(parent=None)
    return categories


@register.simple_tag()
def get_sorted():
    sorters = [
        {
            'title': "Narxi boyicha",
            'sorters': [
                ['price', "O'sish"],
                ['-price', "Kamayish"]
            ]
        },

        {
            'title': "Rangi/Material",
            'sorters': [
                ['colour', "A-Z"],
                ['-colour', "Z-A"]
            ]
        },

        {
            'title': "O'lchovi",
            'sorters': [
                ['size', "O'sish"],
                ['-size', "Kamayish"]
            ]
        }
    ]
    return sorters

@register.simple_tag()
def get_favourite_products(user):
    fav = FavouriteProducts.objects.filter(user=user)
    products = [i.product for i in fav]
    return products

