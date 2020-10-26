from django.db import models

class UploadFile(models.Model):
	uploaded = models.FileField()
	timestamp = models.DateTimeField(auto_now_add = True)
