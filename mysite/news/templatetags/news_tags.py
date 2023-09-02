from django import template
from news.models import Category
from django.db.models import Count, F
from django.core.cache import cache

register = template.Library()


@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_categories(arg1='Hello ', arg2='World'):
    # categories = Category.objects.all()
    categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)

    # categories = cache.get('categories') # Кэширование в более читабельный способ
    # if not categories:
    #     categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
    #     cache.set('categories', categories, 30)

    # categories = cache.get_or_set('categories',
    #                               Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(
    #                                   cnt__gt=0), 30)   # Кэширование одним методом ( не читабельно)

    return {
        'categories': categories,
        'arg1': arg1,
        'arg2': arg2
    }
