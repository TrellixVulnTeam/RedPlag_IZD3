from .serializers import FileSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import UploadFile, OutputFile
import files.moss as pro
import files.wordembeddingpro as word
import files.moss_location as general
from django.core.files import File
from django.conf import settings
from django.http import HttpResponse
import os

class FileView(APIView):
	parser_classes = (MultiPartParser, FormParser)
	permission_classes = (IsAuthenticated,)
	authentication_class = JSONWebTokenAuthentication

	def get(self, request, format = None):
                print(os.getcwd())
                queryset = UploadFile.objects.filter(user=request.user)
                recent = queryset[len(queryset)-1].uploaded.path
                stub = queryset[len(queryset)-1].boilerplate

                if stub.name == '': stub_code = 'None.txt'
                else: stub_code = stub.path
                
                mode = queryset[len(queryset)-1].fileType
                if mode == 'cpp': pro.moss_given_files(recent, stub_code, stub.name == '',1)
                elif mode == 'python': pro.moss_given_files(recent, stub_code, stub.name == '',2)
                elif mode == 'text': word.embedding_process_files(recent)
                elif mode == 'moss': general.moss_given_files(recent)
                filelist = [file.uploaded.name for file in queryset]
                return Response(filelist[-1])

	def post(self, request, *args, **kwargs):
		file_serializer = FileSerializer(data=request.data)
		print(file_serializer)

		if file_serializer.is_valid():
			print("yes valid")
			file_serializer.save(user=self.request.user)
			return Response(file_serializer.data, status=status.HTTP_201_CREATED)
		else:
			print("invalid")
			return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GraphView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_class = JSONWebTokenAuthentication
	def get(self, request, format = None):
		queryset = UploadFile.objects.filter(user=request.user)
		recent = queryset[len(queryset)-1].uploaded.path
		#process_given_files(recent)
		print(os.getcwd())
		os.chdir(settings.BASE_DIR)
		f = open('media/' + os.path.basename(recent).split('.')[0] + 'other.zip','rb')
		print(os.getcwd())
		myfile = File(f)
		queryset[len(queryset)-1].outputfile_set.create(textoutput = myfile)
		file_path= 'media/' + os.path.basename(recent).split('.')[0] + 'other.zip'
		print(os.getcwd())
		f.close()
		with open(file_path, 'rb') as f:
                        print(os.getcwd())
                        response = HttpResponse(f, content_type='application/zip')
                        response['Content-Disposition'] = 'attachment; filename="%s"' % file_path
                        return response

class HeatMapView(APIView):
		permission_classes = (IsAuthenticated,)
		authentication_class = JSONWebTokenAuthentication

		def get(self, request, format = None):
			queryset = UploadFile.objects.filter(user=request.user)
			recent = queryset[len(queryset)-1].uploaded.path
			#process_given_files(recent)
			print(os.getcwd())
			os.chdir(settings.BASE_DIR)
			f = open('media/' + os.path.basename(recent).split('.')[0] + 'other/Graphs/heat_map.png','rb')
			print(os.getcwd())
			myfile = File(f)
			queryset[len(queryset)-1].heatmapfile_set.create(hmapoutput = myfile)
			file_path='media/' + os.path.basename(recent).split('.')[0] + 'other/Graphs/heat_map.png'
			f.close()
			with open(file_path, 'rb') as f:
                                print(os.getcwd())
                                response = HttpResponse(f, content_type='image/png')
                                response['Content-Disposition'] = 'attachment; filename="%s"' % file_path
                                return response

class HistogramView(APIView):
		permission_classes = (IsAuthenticated,)
		authentication_class = JSONWebTokenAuthentication

		def get(self, request, format = None):
			queryset = UploadFile.objects.filter(user=request.user)
			recent = queryset[len(queryset)-1].uploaded.path
			#process_given_files(recent)
			os.chdir(settings.BASE_DIR)
			f = open('media/' + os.path.basename(recent).split('.')[0] + 'other/Graphs/histogram.png','rb')
			myfile = File(f)
			queryset[len(queryset)-1].histogramfile_set.create(histoutput = myfile)
			file_path='media/' + os.path.basename(recent).split('.')[0] + 'other/Graphs/histogram.png'
			f.close()
			with open(file_path, 'rb') as f:
				response = HttpResponse(f, content_type='image/png')
				response['Content-Disposition'] = 'attachment; filename="%s"' % file_path
				return response
