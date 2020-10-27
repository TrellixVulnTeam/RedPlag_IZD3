import uuid
from backend.app.user.models import User
from django.db import models

def random_filename(instance, filename):
  extension = filename.split(".")[-1]
  return "{}.{}".format(uuid.uuid4(), extension)

class UploadFile(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upload_files')
	uploaded = models.FileField('uploaded file', upload_to = random_filename)
	timestamp = models.DateTimeField(auto_now_add = True)
