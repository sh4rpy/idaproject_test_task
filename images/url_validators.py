import mimetypes


VALID_IMAGE_MIMETYPES = [
    'image',
]

VALID_IMAGE_EXTENSIONS = [
    '.jpg',
    '.jpeg',
    '.png',
]


def valid_url_mimetype(url: str, mimetype_list: list[str] = None) -> bool:
    """Проверяет, валиден ли медиа тип у загружаемого по ссылке файла"""
    if mimetype_list is None:
        mimetype_list = VALID_IMAGE_MIMETYPES
    mimetype, encoding = mimetypes.guess_type(url)
    if mimetype:
        return any([mimetype.startswith(m) for m in mimetype_list])
    else:
        return False


def valid_url_extension(url: str, extension_list: list[str] = None) -> bool:
    """Проверяет, валидно ли расширение у загружаемого по ссылке файла"""
    if extension_list is None:
        extension_list = VALID_IMAGE_EXTENSIONS
    return any([url.endswith(e) for e in extension_list])
