
from rest_framework.response import Response


class Response(Response):
    def __init__(self, data=None, status=None, template_name=None, headers=None, exception=False, content_type=None):
        super().__init__(data, status, template_name, headers, exception, content_type)


class DataResponse(Response):
    def __init__(self, data=None, status=None, template_name=None, headers=None, exception=False, content_type=None):
        super().__init__(data, status, template_name, headers, exception, content_type)
        self.data = {'data': data}


class ErrorResponse(Response):
    def __init__(self, data=None, status=None, template_name=None, headers=None, exception=False, content_type=None):
        super().__init__(data, status, template_name, headers, exception, content_type)
        if isinstance(self.data, list):
            errors = []
            for e in self.data:
                errors.append({'detail': e})
            self.data = {'errors': errors}
        else:
            self.data = {'errors': [{'detail': data}]}
