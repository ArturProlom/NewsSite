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
            messages.success(request, 'Registration was successful')
            return redirect('home')
        else:
            messages.error(request, 'Registration error')
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


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'bemben1@ukr.net',
                             ['az0972507926@gmail.com'], fail_silently=True)
            # на стадии деплоя fail_silently = True
            if mail:
                messages.success(request=request, message='Email send')
                return redirect('contact')
            else:
                messages.error(request=request, message='Sending error')
        else:
            messages.error(request=request, message='Validation error')
    else:
        form = ContactForm()
    return render(request=request, template_name='news/contact.html', context={'form': form})


class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    # mixin_prop = 'hello, world'
    paginate_by = 2

    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):  # переопределяем метод
        context = super().get_context_data(**kwargs)
        context['title'] = 'Main page'
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


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # login_url = '/admin/' #редиректит на указанный адрес

    raise_exception = True  # ошибку для неавторизованного
