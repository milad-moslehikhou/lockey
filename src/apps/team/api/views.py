from rest_framework.views import APIView


class TeamsView(APIView):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class TeamView(APIView):
    def get(self, request, pk, *args, **kwargs):
        pass

    def patch(self, request, pk, *args, **kwargs):
        pass

    def delete(self, request, pk, *args, **kwargs):
        pass
