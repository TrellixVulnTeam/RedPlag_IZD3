from django.conf.urls import url
from backend.app.user.views import UserRegistrationView, ChangePasswordView, UserLoginView, DeleteUserView

urlpatterns = [
  url(r'^signup', UserRegistrationView.as_view()),
  url(r'^signin', UserLoginView.as_view()),
  url(r'^change_pass', ChangePasswordView.as_view()),
  url(r'^delete_user', DeleteUserView.as_view()),
]