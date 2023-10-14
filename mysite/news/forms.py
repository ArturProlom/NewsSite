from django import forms
from news.models import Category, News
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField, CaptchaTextInput


class ContactForm(forms.Form):
    subject = forms.CharField(label='Email subject', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Text', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    captcha = CaptchaField()


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}),
                               help_text='Maximum 150 characters')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))



# Форма связанная с моделями
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = '__all__'   # С помощью магического метода получить можно все поля формы
        fields = ('title', 'content', 'is_published', 'category')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        widgets['category']

    captcha = CaptchaField()

    def clean_title(self):  # кастомный валидатор
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Name should not start with a number')
        return title

# class NewsForm(forms.Form):  #  Форма не связанная с моделями
#     title = forms.CharField(max_length=150, label='Название', widget=forms.TextInput(
#         attrs={'class': 'form-control'}
#     ))
#     content = forms.CharField(label='Текст', required=False, widget=forms.Textarea(
#         attrs={'class': 'form-control',
#                'rows': 5
#                }))
#     is_published = forms.BooleanField(label='Опубликовано?', initial=True)
#     category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Выбор категории',
#                                       widget=forms.Select(attrs={'class': 'form-control'}))
#
