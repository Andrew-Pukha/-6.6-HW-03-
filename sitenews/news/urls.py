#-- 2-ОЙ по Счёту urls.py.

from django.contrib import admin
from django.urls import path, re_path, register_converter
from . import converters
from news import views
from .views import NewsCategory

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.MainPage.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('login/', views.login, name='login'),

    path('category/<slug:cat_slug>/', NewsCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('edit/<int:pk>/', views.UpdatePage.as_view(), name='edit_page'),
]