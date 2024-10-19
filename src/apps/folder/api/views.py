from django.db.models import RestrictedError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from apps.folder.models import Folder
from apps.folder.api.serializers import FolderSerializer, FolderTreeSerializer


class FolderViewSet(ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    filterset_fields = ['is_public', 'parent', 'user']
    search_fields = None
    ordering_fields = ['id']
    ordering = ['-id']

    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissions
    ]

    @action(
        methods=['GET'],
        url_name="tree",
        url_path="tree",
        detail=False
    )
    def get_folder_tree(self, request):
        user = request.user
        public = Folder.objects.filter(is_public=True)
        private = Folder.objects.filter(user=user, is_public=False)
        data = {
            'public': self._get_folder_children(public),
            'private': self._get_folder_children(private)
        }
        serializer = FolderTreeSerializer(data)
        return Response(serializer.data)

    def _get_folder_children(self, folders, parent_id=None):
        item = []
        for folder in folders:
            if folder.parent_id == parent_id:
                sub_folders = folder.child.all()
                item.append({
                    'folder': folder,
                    'children': self._get_folder_children(sub_folders, parent_id=folder.id)
                })
        return item

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except RestrictedError:
            raise ValidationError(
                "Folder is not empty, delete them first",
                "restericted-field")
