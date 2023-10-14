from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Name')
    content = models.TextField(blank=True, verbose_name='Content')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Publication date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Photo', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Published')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Category')
    views = models.IntegerField(default=0)
    # related_name='get_news' в категории   default =  model_name_set

    # в данном случае это вторичная модель , а Category  - первичная
    #
    # def get_absolute_url(self):
    #     return reverse(viewname='view_news', kwargs={'news_id': self.pk})

    # get_absolute_url  название метода по конвенции джанго
    def get_absolute_url(self):
        return reverse(viewname='view_news', kwargs={'pk': self.pk})

    # редирект в views.py CreateNews  роисходит благодаря переопределению get_absolute_url

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'New'
        verbose_name_plural = 'News'
        ordering = ['-created_at']


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Category`s name')

    def get_absolute_url(self):
        return reverse(viewname='category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']
