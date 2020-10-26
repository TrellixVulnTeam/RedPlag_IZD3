from rest_framework import viewsets, filters
from .serializers import FileSerializer
from .models import UploadFile

class FileView(viewsets.ModelViewSet):
        queryset = UploadFile.objects.all()
        serializer_class = FileSerializer
