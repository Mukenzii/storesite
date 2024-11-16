from django import template
from store.models import Category



register = template.Library()

@register.simple_tag()
def get_categories():
    categories = Category.objects.filter(parent=None)
    return categories

@register.simple_tag()
def get_sorted():
    sorters = [
        {
            'title': "Narxi bo'yicha",
            'sorters': [
                ['price', "O'sish"],
                ['-price', 'Kamayish']
            ]
        },
        {
            'title': "Rangi/Material",
            'sorters': [
                ['colour', "A-Z"],
                ['-colour', 'Z-A']
            ]
        },
        {
            'title': "O'lchovi",
            'sorters': [
                ['size', "O'sish"],
                ['-size', 'Kamayish']
            ]
        }
    ]
    return sorters


