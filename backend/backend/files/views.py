from .serializers import FileSerializer
from .models import UploadFile
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from backend.app.profile.models import UserProfile

class FileView(APIView):
	parser_classes = (MultiPartParser, FormParser)
	permission_classes = (IsAuthenticated,)
	authentication_class = JSONWebTokenAuthentication

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