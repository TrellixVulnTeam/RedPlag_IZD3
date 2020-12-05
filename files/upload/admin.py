from django.contrib import admin
from .models import UploadFile, OutputFile, HeatMapFile, HistogramFile
admin.site.register(UploadFile)
admin.site.register(OutputFile)
admin.site.register(HeatMapFile)
admin.site.register(HistogramFile)

