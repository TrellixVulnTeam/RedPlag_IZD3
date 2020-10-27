from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import FileSerializer
from .models import UploadFile
from .plag_detect import *

class FileView(viewsets.ModelViewSet):
        queryset = UploadFile.objects.all()
        serializer_class = FileSerializer

        @action(detail=True, methods=['post'])
        def process_plag(self, request):
                print(self.queryset[0].uploaded.name)
                process_given_files(self.queryset[0].uploaded.name)
