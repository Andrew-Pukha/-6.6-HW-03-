from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .models import *
from django.core.validators import MinLengthValidator, MaxLengthValidator






#-- #46. СОЗДАНИЕ ПОЛЬЗОВАТЕЛЬСКОГО ВАЛИДАТОРА.
#-- Наш валидатор будет проверять, чтобы в данных присутствовали только русские символы, цифры, дефис и пробел.
#-- Другие символы будем считать недопустимыми. Для этого определим валидатор следующим образом:
@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code, params={"value": value})














#-- #44. Следующий шаг – объявить класс AddPostForm, описывающий форму добавления статьи.
#-- Он будет унаследован от базового класса Form и иметь следующий вид:

#-- атрибуты (title, slug, content и т.д.) нужно называть также, как в атрибуты класса News()\models.py.
class AddPostForm(forms.ModelForm):

    #-- #47. Связывание аргументов из forms.py c models.py для того, чтобы код не дублировался (для этого весь предыдущий код должен быть закомментирован):
    # title = forms.CharField(max_length=255, min_length=5,      #-- #46.Аргументы для установки минимальной и максимальной длины Заголовка создаваемой Новости\Статьи.
    #                         label="Заголовок",
    #                         widget=forms.TextInput(attrs={'class': 'form-input'}),
    #                         validators=[
    #                             RussianValidator(),
    #                         ],
    #                         error_messages={
    #                             'min_length': 'Слишком короткий заголовок',
    #                             'requied': 'Без заголовка никак'
    #                         })
    # slug = forms.SlugField(max_length=255, label="URL",
    #                        validators=[
    #                            MinLengthValidator(55, message="Нужно минимум 5 символов"),       #-- #46. Параметры для установки минимальной и максимальной длины (другой способ в отличии от способа выше) Slug-а создаваемой Новости\Статьи.
    #                            MaxLengthValidator(100, message="Нужно максимум 100 символов"),
    #                        ])
    # content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label="Содержание")
    # is_published = forms.BooleanField(required=False, initial=True, label="Опубликовано\Не опубликовано")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана', label="Категории")
    author = forms.ModelChoiceField(queryset=Author.objects.all(), empty_label='Материал без автора', required=False, label="Автор")

    class Meta:
        model = News
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'author', 'tags']  # -- атрибут fields будет содержать все те поля, что и у Модели News().
        labels = {'slug': 'URL'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    #-- #47. СОЗДАНИЕ СОБСТВЕННЫХ ВАЛИДАТОРОВ ФОРМЫ.
    #-- #47. Опишем валидатор для поля title, который бы не позволял вводить строку более 50 символов.
    #-- Как я уже отметил в SQLite эта проверка не проходит, а просто обрезается заголовок до указанной длины,
    #-- а мы сделаем так, что пользователю будет показываться сообщение, что название статьи слишком большое.
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')

        return title










#-- #48. Класс поля FileField

#-- #48. До класса UploadFileForm() поля формы никак не проверялись на корректность (валидность), загрузили мы файл или нет - ошибки не возникало;
#-- нужно это исправить:

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")