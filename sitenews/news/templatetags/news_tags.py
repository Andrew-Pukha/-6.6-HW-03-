from django import template
from django.db.models import Count

import news.views as views
from news.models import *

register = template.Library()

#-- Ниже прописан простой ТЭГ, тэг который задаёт маршрут категориям материала (новостям или статьям):
#@register.simple_tag()
#def get_categories():
    #return views.cats_db



#-- Ниже прописан включащий ТЭГ, тэг который открывает категорию материала (новость или статью):
@register.inclusion_tag('news/list_categories.html')   #-- В качестве аргумента указываем путь к шаблону,
                                                       #-- который будет открываться этим ТЭГом, и в этот шаблон будет передаваться список-cats_db:
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)    #-- До #27 Отображения постов по рубрикам: cats = views.cats_db. | #35 Часть данной строки, а именно: annotate(total=Count("posts")).filter(total__gt=0) выводит только те РУБРИКИ, КОТОРЫЕ ЗАПОЛНЕНЫ МАТЕРИАЛОМ.
    return {'cats': cats, 'cat_selected': cat_selected}





#-- #29. Cформируем новый шаблонный тег для отображения списка тегов в сайдбаре.
#-- Откроем файл news/news_tags.py и зарегистрируем еще одну функцию:
@register.inclusion_tag('news/list_tags.html')
def show_all_tags():
    return {"tags": TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}    #-- Часть данной строки, а именно: annotate(total=Count("tags")).filter(total__gt=0)} выводит только те ТЕГИ, К КОТОРЫМ ЧТО-ТО ПРИКРЕПЛЕНО.
