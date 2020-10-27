import uuid
from django.db import models
from .plag_detect import *

def random_filename(instance, filename):
        extension = filename.split(".")[-1]
        zip_dir_loc = "{}.{}".format(uuid.uuid4(), extension)
        return zip_dir_loc

class UploadFile(models.Model):
	uploaded = models.FileField('uploaded file', upload_to = random_filename)
	timestamp = models.DateTimeField(auto_now_add = True)
