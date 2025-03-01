from rest_framework.response import Response


class ClientErrorResponse(Response):
    def __init__(self, data=None, status=None, template_name=None, headers=None, exception=False, content_type=None):  # noqa: PLR0913
        _data = {"type": "client_error", "errors": [{"detail": data}]}
        super().__init__(_data, status, template_name, headers, exception, content_type)
