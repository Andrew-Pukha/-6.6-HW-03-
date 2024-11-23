"""
URL configuration for sitenews project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
#-- 1-ЫЙ по Счёту urls.py.
from django.contrib import admin
from django.urls import path, include

from news.views import page_not_found
from sitenews import settings

handler404 = page_not_found
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),   #-- данная строка может добавлять любой суффикс (или без суффикса)
                                      #-- к доменному адрему адресу, например: http://127.0.0.1:8000/news/ или http://127.0.0.1:8000/news/cats/.
    path("__debug__/", include("debug_toolbar.urls")),
]



#-- #50. Определяем маршрут "выдачи" файлов, т.е., мы говорим, если веб-сервер работает в режиме отладки,
#-- то в список маршрутов нужно добавить еще один маршрут, с префиксом media, и связать его с каталогом MEDIA_ROOT, где эти файлы расположены, чтобы в конечном итоге, файлы выводились на сайте.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






#-- #37. Немного настроим админ-панель, чтобы она выглядела приятнее и дружелюбнее.
#-- Первое, что мы сделаем – это заменим заголовок админки на наше собственное.
admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Новости и статьи"