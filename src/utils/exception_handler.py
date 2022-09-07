from rest_framework.views import exception_handler


def api_exception(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc.detail, (list, dict)):
            response.data = exc.detail
        else:
            response.data = {'message': exc.detail}

    return response
