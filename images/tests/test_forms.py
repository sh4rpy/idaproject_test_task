import shutil
import tempfile

from django.conf import settings
from django.shortcuts import reverse
from django.test import TestCase, Client

from ..models import Image


class TestUploadForm(TestCase):
    @classmethod
    def setUpClass(cls):
        """Создаем временную папку для медиафайлов"""
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

    @classmethod
    def tearDownClass(cls):
        """Удаляем временную папку"""
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.client = Client()
        self.url = 'https://upload.wikimedia.org/wikipedia/commons/9/95/MrRobot_intertitle.png'
        self.image_count = Image.objects.count()

    def test_upload_image_from_computer(self):
        """Проверяем, создается ли запись при загрузке с компьютера"""
        with open('images/tests/test.png', 'rb') as fp:
            self.client.post(reverse('upload'), data={'original_image': fp})
        self.assertEqual(Image.objects.count(), self.image_count + 1, 'Запсиь не создалась')

    def test_upload_image_from_url(self):
        """Проверяем, создается ли запись при загрузке через URL"""
        self.client.post(reverse('upload'), data={'url': self.url})
        self.assertEqual(Image.objects.count(), self.image_count + 1, 'Запсиь не создалась')

    def test_upload_image_with_wrong_form_data(self):
        """
        Проверяем, что при отправке невалидной формы
        запись не создается и возбуждается ошибка
        """
        with open('images/tests/test.png', 'rb') as fp:
            response = self.client.post(
                reverse('upload'), data={'original_image': fp, 'url': self.url}
            )
        self.assertEqual(Image.objects.count(), self.image_count, 'Запись создалась, а не должна')
        self.assertFormError(response, 'form', None,
                             'Невозможно одновременно загрузить изображение и по ссылке, и с компьютера',
                             'Форма не содержит такой ошибки')

    def test_upload_image_with_empty_form_data(self):
        """
        Проверяем, что при отправке пустой формы
        запись не создается и возбуждается ошибка
        """
        response = self.client.post(
            reverse('upload'), data={}
        )
        self.assertEqual(Image.objects.count(), self.image_count, 'Запись создалась, а не должна')
        self.assertFormError(response, 'form', None, 'Хотя бы одно поле должно быть заполнено',
                             'Форма не содержит такой ошибки')


class TestResizeForm(TestCase):
    @classmethod
    def setUpClass(cls):
        """Создаем временную папку для медиафайлов"""
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

    @classmethod
    def tearDownClass(cls):
        """Удаляем временную папку"""
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.client = Client()
        with open('images/tests/test.png', 'rb') as fp:
            self.client.post(reverse('upload'), data={'original_image': fp})
        self.image = Image.objects.first()

    def test_resize_image_height(self):
        """Проверяем, что высота изображения меняется"""
        self.client.post(reverse('update', kwargs={'pk': self.image.pk}),
                         data={'height': 100})
        resized_image = Image.objects.first()
        self.assertEqual(resized_image.resized_image.height, 100, 'Высота не изменилась')

    def test_resize_image_width(self):
        """Проверяем, что ширина изображения меняется"""
        self.client.post(reverse('update', kwargs={'pk': self.image.pk}),
                         data={'height': 100})
        resized_image = Image.objects.first()
        self.assertEqual(resized_image.resized_image.height, 100, 'Ширина не изменилась')
