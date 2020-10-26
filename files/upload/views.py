from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
from .models import UploadFile

class FileView(viewsets.ModelViewSet):
        queryset = UploadFile.objects.all()
        serializer_class = FileSerializer
        parser_classes = (MultiPartParser, FormParser)

        def post(self, request, *args, **kwargs):
                file_serializer = FileSerializer(data = request.data)
                if file_serializer.is_valid():
                        file_serializer.save()
                        return Response(file_serializer.data, status = status.HTTP_201_CREATED)
                else:
                        return Response(file_serializer.errors, status = status.HTTP_404_BAD_REQUEST)
