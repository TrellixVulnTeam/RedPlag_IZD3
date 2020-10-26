from django.conf.urls import url,include
from rest_framework import routers
from .viewsets import FileView

router = routers.DefaultRouter()
router.register('files',FileView,'files')

urlpatterns = [
	url(r'^', include(router.urls)),
]
