from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from apps.folder.models import Folder


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = "__all__"


class FolderChildSerializer(serializers.Serializer):
    folder = FolderSerializer()
    children = serializers.ListField(child=RecursiveField("FolderSerializer"))


class FolderTreeSerializer(serializers.Serializer):
    private = FolderChildSerializer(many=True, read_only=True)
    public = FolderChildSerializer(many=True, read_only=True)
