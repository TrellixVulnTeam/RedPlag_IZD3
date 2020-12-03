import uuid
from backend.app.user.models import User
from django.db import models
from django.conf import settings

def random_filename(instance, filename):
  extension = filename.split(".")[-1]
  return "{}.{}".format(uuid.uuid4(), extension)

class UploadFile(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='upload', db_column="user")
	uploaded = models.FileField(blank=False, null=False)
	timestamp = models.DateTimeField(auto_now_add = True)
	boilerplate = models.FileField(blank = True, null = True)

	def __str__(self):
		return '{} ({})'.format(self.uploaded)

class OutputFile(models.Model):
	zipfile = models.ForeignKey(UploadFile, on_delete = models.CASCADE)
	textoutput = models.FileField()
