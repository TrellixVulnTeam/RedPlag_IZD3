import uuid
from backend.app.user.models import User
from django.db import models
from django.conf import settings

def random_filename(instance, filename):
	"""
	Generates random filename and return it
	"""
	extension = filename.split(".")[-1]
	return "{}.{}".format(uuid.uuid4(), extension)

class UploadFile(models.Model):
	"""
	Model to store the uploaded file and it's other attributes
	"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='upload', db_column="user")
	uploaded = models.FileField(blank=False, null=False)
	timestamp = models.DateTimeField(auto_now_add = True)
	boilerplate = models.FileField(blank = True, null = True)
	fileType = models.CharField(default = 'text', max_length = 6)

	def __str__(self):
		return '{} ({})'.format(self.uploaded)

class OutputFile(models.Model):
	"""
	Model to store the files/graphs generated after processing which will be available for download 
	"""
	zipfile = models.ForeignKey(UploadFile, on_delete = models.CASCADE)
	textoutput = models.FileField()

class HeatMapFile(models.Model):
	"""
	Model to store the heatmap which will be eventually displayed on the webpage
	"""
	zipfile = models.ForeignKey(UploadFile, on_delete = models.CASCADE)
	hmapoutput = models.ImageField()

class HistogramFile(models.Model):
	"""
	Model to store the histogram which will be eventually displayed on the webpage
	"""
	zipfile = models.ForeignKey(UploadFile, on_delete = models.CASCADE)
	histoutput = models.ImageField()
