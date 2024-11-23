from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView

from .forms import AddPostForm, UploadFileForm
from .models import *
from .utils import DataMixin, menu


class MainPage(DataMixin, ListView):

    template_name = 'news/main_page.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return News.published.all().select_related('cat')



def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'news/about.html', {'title': 'О сайте', 'menu': menu, 'form': form})



class ShowPost(DataMixin, DetailView):
    template_name = 'news/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'])

    def get_object(self, queryset=None):
        return get_object_or_404(News.published, slug=self.kwargs[self.slug_url_kwarg])




class NewsCategory(DataMixin, ListView):
    template_name = 'news/main_page.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.id,
                                      )

    def get_queryset(self):
        return News.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')




class TagPostList(DataMixin, ListView):
    template_name = 'news/main_page.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return News.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')










def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class AddPage(DataMixin, FormView):
    form_class = AddPostForm
    template_name = 'news/addpage.html'
    title_page = 'Добавление статьи'

class UpdatePage(DataMixin, UpdateView):
    model = News
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'news/addpage.html'
    success_url = reverse_lazy('home')
    title_page = "Редактирование статьи"



def contact(request):
    return HttpResponse("Связяться с нами")

def login(request):
    return HttpResponse("Авторизация на сайте")




