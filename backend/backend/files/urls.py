from django.conf.urls import url,include
from files.views import FileView

urlpatterns = [
	url(r'^', FileView.as_view()),
]