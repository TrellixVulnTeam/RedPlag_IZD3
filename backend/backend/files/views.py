from .serializers import FileSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import UploadFile, OutputFile
from .moss import *
from .wordembeddingpro import *
from django.core.files import File
from django.conf import settings
from django.http import HttpResponse
import os

class FileView(APIView):
	"""
	Api endpoint to upload file and download the uploaded file
	URL: http://127.0.0.1:8000/file/upload
	"""
	parser_classes = (MultiPartParser, FormParser)
	permission_classes = (IsAuthenticated,)
	authentication_class = JSONWebTokenAuthentication

	def get(self, request, format = None):
		"""
		Api endpoint to process the uploaded files depending upon it's type
		and generate results which are available for download
		"""
    print(os.getcwd())
    queryset = UploadFile.objects.filter(user=request.user)
    recent = queryset[len(queryset)-1].uploaded.path
    stub = queryset[len(queryset)-1].boilerplate

    if stub.name == '': stub_code = 'None.txt'
    else: stub_code = stub.path
    
    mode = queryset[len(queryset)-1].fileType
    if mode == 'cpp': moss_given_files(recent, stub_code, stub.name == '',1)
    elif mode == 'python': moss_given_files(recent, stub_code, stub.name == '',2)
    elif mode == 'text': embedding_process_files(recent)
    filelist = [file.uploaded.name for file in queryset]
    return Response(filelist[-1])

	def post(self, request, *args, **kwargs):
		"""
		Api endpoint to upload the zip file
		"""
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
	"""
	Api endpoint to download the results after processing in the form of zip file containing heatmap, csv file and histogram
	URL: http://127.0.0.1:8000/file/results
	"""
	permission_classes = (IsAuthenticated,)
	authentication_class = JSONWebTokenAuthentication
	def get(self, request, format = None):
		"""
		Request type: GET
		Sends the zip file which is available for download
		Content type: application/zip
		"""
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
		"""
		API endpoint to send the heatmap image to frontend for visualization on the webpage
		URL: http://127.0.0.1:8000/file/heatmap
		"""
		permission_classes = (IsAuthenticated,)
		authentication_class = JSONWebTokenAuthentication

		def get(self, request, format = None):
			"""
			Request type: GET
			Send the heatmap image as Http response with content_type as image/png
			"""
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
		"""
		API endpoint to send the histogram image to frontend for visualization on the webpage
		URL: http://127.0.0.1:8000/file/histogram
		"""
		permission_classes = (IsAuthenticated,)
		authentication_class = JSONWebTokenAuthentication

		def get(self, request, format = None):
			"""
			Request type: GET
			Send the histogram image as Http response with content_type as image/png
			"""
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
