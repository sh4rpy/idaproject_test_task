import shutil
import tempfile

from django.conf import settings
from django.shortcuts import reverse
from django.test import TestCase, Client

from ..models import Image


class TestUrls(TestCase):
    @classmethod
    def setUpClass(cls):
        """Создаем временуую папку для медиафайлов"""
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

    @classmethod
    def tearDownClass(cls):
        """Удаляет временную папку"""
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.client = Client()
        with open('images/tests/test.png', 'rb') as fp:
            self.client.post(reverse('upload'), data={'original_image': fp})
        self.image = Image.objects.first()

    def test_availability_of_all_pages(self):
        """Проверяет доступность всех страниц"""
        urls = {
            '/': reverse('index'),
            'upload': reverse('upload'),
            'update': reverse('update', kwargs={'pk': self.image.pk}),
        }
        for url, reverse_name in urls.items():
            with self.subTest(url=url):
                response = self.client.get(reverse_name)
                self.assertEqual(response.status_code, 200)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответсвующий шаблон"""
        templates_url_names = {
            reverse('index'): 'index.html',
            reverse('upload'): 'images/upload.html',
            reverse('update', kwargs={'pk': self.image.pk}): 'images/update.html',
        }
        for reverse_name, template in templates_url_names.items():
            with self.subTest(template=template):
                response = self.client.get(reverse_name)
                self.assertTemplateUsed(response, template)
