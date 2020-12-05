import uuid
from django.db import models

def random_filename(instance, filename):
        extension = filename.split(".")[-1]
        zip_dir_loc = "{}.{}".format(uuid.uuid4(), extension)
        return zip_dir_loc

class UploadFile(models.Model):
	uploaded = models.FileField(upload_to = random_filename)
	timestamp = models.DateTimeField(auto_now_add = True)

class OutputFile(models.Model):
        zipfile = models.ForeignKey(UploadFile, on_delete = models.CASCADE)
        textoutput = models.FileField()

class HeatMapFile(models.Model):
	zipfile = models.ForeignKey(UploadFile, on_delete = models.CASCADE)
	hmapoutput = models.ImageField()

class HistogramFile(models.Model):
	zipfile = models.ForeignKey(UploadFile, on_delete = models.CASCADE)
	histoutput = models.ImageField()
        
