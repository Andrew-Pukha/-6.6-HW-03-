from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import *





class AuthordFilter(admin.SimpleListFilter):
    title = 'Статус материала'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('have_author', 'У данного материала есть автор'),
            ('have_not_author', 'У данного материала нет автора'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'have_author':
            return queryset.filter(author__isnull=False)
        elif self.value() == 'have_not_author':
            return queryset.filter(author__isnull=True)







@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'author', 'tags']
    readonly_fields = ['post_photo']
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ['tags']
    list_display = ('id', 'title', 'post_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('id', 'title')
    ordering = ['-time_create', 'title']
    list_editable = ('is_published', )
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = [AuthordFilter, 'cat__name', 'is_published']
    save_on_top = True

    @admin.display(description="Изображение")
    def post_photo(self, women: News):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return "Без фото"


    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=News.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=News.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!", messages.WARNING)





@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

