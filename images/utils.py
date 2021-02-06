import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile

from .models import Image as ImageModel


def resize_image(source: ImageModel, width: int, height: int) -> None:
    """Изменяет размер исходного изображения"""
    if width is None:
        width = height
    if height is None:
        height = width
    output_io_stream = BytesIO()
    image = Image.open(source.original_image)
    image.thumbnail((width, height), Image.BILINEAR)
    os.remove(source.resized_image.path)
    image.save(output_io_stream, format=image.format, quality=100)
    content = ContentFile(output_io_stream.getvalue(), source.get_file_name)
    source.resized_image = content
    source.save()
    output_io_stream.close()
