from django.conf.urls import url,include
from rest_framework import routers
from .viewsets import FileView

router = routers.DefaultRouter()
router.register('files',FileView,'files')
process_file = FileView.as_view({
    'get':'list',
    'post': 'process_plag'
})

urlpatterns = [
	url(r'^', include(router.urls)),
        url(r'^plag', process_file, name = 'process-file')
]
