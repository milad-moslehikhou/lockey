import logging

from django.core.management.color import color_style


class ColoredFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super(ColoredFormatter, self).__init__(*args, **kwargs)
        self.style = color_style()
        self.style.DEBUG = self.style.HTTP_NOT_MODIFIED
        self.style.INFO = self.style.HTTP_INFO
        self.style.WARNING = self.style.WARNING
        self.style.ERROR = self.style.ERROR
        self.style.CRITICAL = self.style.HTTP_SERVER_ERROR

    def format(self, record):
        message = logging.Formatter.format(self, record)
        colorizer = getattr(self.style, record.levelname, self.style.SUCCESS)
        return colorizer(message)

