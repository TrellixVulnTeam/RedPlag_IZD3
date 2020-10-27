from rest_framework import serializers
from .models import UploadFile

class FileSerializer(serializers.ModelSerializer):
	class Meta():
		model = UploadFile
		fields = ('owner','uploaded','timestamp')
