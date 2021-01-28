import os
from urllib.request import urlretrieve

from django.core.files import File
from django.db import models


class Image(models.Model):
    """Модель изображения. Храним и оригинальное, и с измененными размерами"""
    original_image = models.ImageField(
        upload_to='images/original/', verbose_name='Файл', blank=True
    )
    resized_image = models.ImageField(upload_to='images/resized/', blank=True)
    url = models.URLField(verbose_name='Ссылка', blank=True)

    @property
    def get_file_name(self):
        """Возвращает имя файла"""
        return os.path.basename(self.resized_image.name)

    def get_image_from_url(self):
        """Загружает изображение через URL, если отсутсвует локальное изображение"""
        str_url = str(self.url)
        if self.url and not self.original_image:
            image = urlretrieve(str_url)
            self.original_image.save(
                os.path.basename(str_url), File(open(image[0], 'rb'))
            )
            self.save()

    def save(self, *args, **kwargs):
        # здесь расширяем родительский метод возможностью сохранение через URL
        self.get_image_from_url()
        super().save(*args, **kwargs)
