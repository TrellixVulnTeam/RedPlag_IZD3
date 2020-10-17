from django.conf.urls import url
from backend.app.profile.views import UserProfileView


urlpatterns = [
  url(r'^profile', UserProfileView.as_view()),
]