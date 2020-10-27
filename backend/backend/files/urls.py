from django.conf.urls import url,include
from files.views import FileView, GraphView

urlpatterns = [
	url(r'^upload/', FileView.as_view(), name='file-upload'),
	url(r'^results/',GraphView.as_view())
]