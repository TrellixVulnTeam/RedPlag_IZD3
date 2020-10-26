import uuid
from django.db import models

def random_filename(instance, filename):
        extension = filename.split(".")[-1]
        return "{}.{}".format(uuid.uuid4(), extension)

class UploadFile(models.Model):
	uploaded = models.FileField('uploaded file', upload_to = random_filename)
	timestamp = models.DateTimeField(auto_now_add = True)
