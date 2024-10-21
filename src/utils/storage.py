from django.conf import settings
from urllib.parse import urljoin
from django.core.files.storage import FileSystemStorage


class ImageStorage(FileSystemStorage):

    def url(self, name):
        return urljoin(settings.BASE_URL, super().url(name))
