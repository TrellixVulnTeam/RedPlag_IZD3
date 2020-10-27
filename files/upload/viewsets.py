from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import FileSerializer
from .models import UploadFile, OutputFile
from .plag_detect import *
from django.core.files import File
from django.conf import settings
from django.http import HttpResponse
import os

class FileView(viewsets.ModelViewSet):
        queryset = UploadFile.objects.all()
        serializer_class = FileSerializer

        @action(detail=True, methods=['get'])
        def process_plag(self, request):
                recent = self.queryset[len(self.queryset)-1].uploaded.path
                process_given_files(recent)
                f = open(os.path.basename(recent).split('.')[0] + 'other.zip','rb')
                myfile = File(f)
                self.queryset[len(self.queryset)-1].outputfile_set.create(textoutput = myfile)
                file_path=os.path.basename(recent).split('.')[0] + 'other.zip'
                f.close()
                with open(file_path, 'rb') as f:
                        response = HttpResponse(f, content_type='application/zip')
                        #response['Content-Disposition'] = 'attachment; filename="%s"' % 'foo.zip'
                        #response = HttpResponse(f, content_type='application/zip')
                        response['Content-Disposition'] = 'attachment; filename="%s"' % file_path
                        return response
