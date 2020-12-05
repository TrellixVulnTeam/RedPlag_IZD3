from django.conf.urls import url,include
from .views import FileView, GraphView, HeatMapView, HistogramView

urlpatterns = [
	url(r'^files', FileView.as_view()),
  url(r'^results',GraphView.as_view()),
  url(r'^heatmap/', HeatMapView.as_view()),
  url(r'^histogram/', HistogramView.as_view())
]
