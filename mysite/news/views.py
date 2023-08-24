from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from news.models import News, Category
from news.forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from django.views.generic import ListView, DetailView, CreateView
from news.utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request=request, user=user)
            messages.success(request, 'Регистрация прошла успешно')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request=request, template_name='news/register.html', context={'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request=request, user=user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request=request, template_name='news/login.html', context={'form': form})


def user_logout(request):
    logout(request)
    return redirect('user_login')


def test(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['content'],
                from_email='az0509623882@ukr.net',
                recipient_list=['az0972507926@gmail.com'],
                fail_silently=False)
            if mail:
                messages.success(request=request, message='Письмо  отправлено')
                return redirect('test')
            else:
                messages.error(request=request, message='Ошибка отправки')
        else:
            messages.error(request=request, message='Форма заполнена неверно!')
    else:
        form = ContactForm()
    return render(request=request, template_name='news/test.html', context={'form': form})


class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    # mixin_prop = 'hello, world'
    paginate_by = 2

    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):  # переопределяем метод
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        # context['title'] = self.get_upper(context['title'])
        # context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):  # переопределяем метод
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):  # переопределяем метод
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'

    # по умолчанию нужно передавать в url pk или slug , но у нас параметр 'news_id' был заменен в url  на pk
    #  в методе  def get_absolute_url(self):
    #         return reverse(viewname='view_news', kwargs={'news_id': self.pk})
    #         мы заменили так же kwargs={'pk': self.pk}
    #  для slug  атрибут - 'slug_url_kwarg'

    # pk_url_kwarg = 'news_id'
    # template_name = 'news/news_detail.html'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # login_url = '/admin/' #редиректит на указанный адрес

    raise_exception = True  # ошибку для неавторизованного

    # reverse  по сути аналог  reverse_lazy с тем отличием что reverse_lazy мы можем использовать в данном месте ,
    #  а reverse   - нет , это аналог в коде  тегу шаблонному url
    # success_url = reverse_lazy('home')

# def index(request):
#     news = News.objects.all()
#     return render(request=request, template_name='news/index.html',
#                   context={
#                       'news': news,
#                       'title': 'Список Новостей '})


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request=request, template_name='news/category.html', context={
#         'news': news,
#         'category': category})


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request=request, template_name='news/view_news.html', context={'news_item': news_item})


# def add_news(request):  # для формы связанной с моделью
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#
#     return render(request=request, template_name='news/add_news.html', context={'form': form})

# def add_news(request):   #  Для формы не связаной с моделью
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             news = News.objects.create(**form.cleaned_data)
#             return redirect(news)
#     else:
#         form = NewsForm()
#
#     return render(request=request, template_name='news/add_news.html', context={'form': form})
