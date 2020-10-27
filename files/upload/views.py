from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FileSerializer
from .models import UploadFile, OutputFile
from .plag_detect import *
from django.core.files import File
from django.conf import settings
from django.http import HttpResponse
import os

class FileView(APIView):
        serializer_class = FileSerializer
        parser_class = (MultiPartParser,FormParser)

        def get(self, request, format = None):
                queryset = UploadFile.objects.all()
                filelist = [file.uploaded.name for file in queryset]
                return Response(filelist)

        def post(self,request,*args, **kwargs):
                file_serializer = FileSerializer(data=request.data)
                if file_serializer.is_valid():
                        file_serializer.save()
                        return Response(file_serializer.data, status=status.HTTP_201_CREATED)
                else: return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GraphView(APIView):
        def get(self, request, format = None):
                queryset = UploadFile.objects.all()
                recent = queryset[len(queryset)-1].uploaded.path
                process_given_files(recent)
                f = open(os.path.basename(recent).split('.')[0] + 'other.zip','rb')
                myfile = File(f)
                queryset[len(queryset)-1].outputfile_set.create(textoutput = myfile)
                file_path=os.path.basename(recent).split('.')[0] + 'other.zip'
                f.close()
                with open(file_path, 'rb') as f:
                        response = HttpResponse(f, content_type='application/zip')
                        response['Content-Disposition'] = 'attachment; filename="%s"' % file_path
                        return response
