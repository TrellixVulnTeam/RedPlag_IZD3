from django.conf.urls import url
from backend.app.user.views import UserRegistrationView, ChangePasswordView, UserLoginView, DeleteUserView
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
  url(r'^api-token-auth/', obtain_jwt_token),
  url(r'^api-token-refresh/', refresh_jwt_token),
  url(r'^api-token-verify/', verify_jwt_token),
  url(r'^signup', UserRegistrationView.as_view()),
  url(r'^login', UserLoginView.as_view()),
  url(r'^change_pass', ChangePasswordView.as_view()),
  url(r'^delete_user', DeleteUserView.as_view()),
]