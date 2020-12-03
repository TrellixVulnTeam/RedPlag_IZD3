from rest_framework import serializers
from .models import UploadFile

class FileSerializer(serializers.ModelSerializer):
	# user = serializers.HiddenField(default=serializers.CurrentUserDefault())
	class Meta():
		model = UploadFile
		fields = ('uploaded','timestamp', 'boilerplate','fileType')
