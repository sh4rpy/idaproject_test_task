from urllib.error import HTTPError
from urllib.request import urlopen

from django import forms
from django.core.exceptions import ValidationError

from .models import Image
from .url_validators import valid_url_mimetype, valid_url_extension


class ImageUploadForm(forms.ModelForm):
    """Форма загрузки изображения"""
    class Meta:
        model = Image
        fields = ('url', 'original_image',)

    def clean(self):
        """Проверка, что только одно поле заполнено"""
        from_url = self.cleaned_data.get('url')
        from_computer = self.cleaned_data.get('original_image')
        if from_url and from_computer:
            raise ValidationError(
                'Невозможно одновременно загрузить изображение и по ссылке, и с компьютера'
            )
        if not from_url and not from_computer:
            raise ValidationError('Хотя бы одно поле должно быть заполнено')
        return self.cleaned_data

    def clean_url(self):
        """Проверка правильности ссылки"""
        url = self.cleaned_data.get('url')
        if url == '':
            return url
        try:
            urlopen(url)
        except HTTPError:
            raise ValidationError('Убедитесь в правильности ссылки')
        if url and not valid_url_mimetype(url) and not valid_url_extension(url):
            raise ValidationError(
                'URL-адрес должен иметь расширение изображения .jpg/.jpeg/.png'
            )
        return url


class ImageResizeForm(forms.Form):
    """Форма изменения размера изображения"""
    width = forms.IntegerField(label='Ширина', required=False)
    height = forms.IntegerField(label='Высота', required=False)

    def clean(self):
        """Проверяет, что хотя бы одно поле заполнено"""
        width = self.cleaned_data['width']
        height = self.cleaned_data['height']
        if not width and not height:
            raise ValidationError('Необходимо заполнить хотя бы одно поле')
        return self.cleaned_data
