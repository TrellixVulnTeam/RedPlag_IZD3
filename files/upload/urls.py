from django.conf.urls import url,include
from .views import FileView, GraphView

urlpatterns = [
	url(r'^files', FileView.as_view()),
        url(r'^results',GraphView.as_view())
]
