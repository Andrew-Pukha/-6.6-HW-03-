from django.apps import AppConfig


class NewsConfig(AppConfig):
    verbose_name = 'Новости/Статьи/Авторские материалы'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
