## @package UserProfile
# @brief Handles request to login, signup, update password and delete user

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from backend.app.user.models import User
from rest_framework.permissions import IsAuthenticated
from backend.app.user.serializers import UserRegistrationSerializer, UserLoginSerializer, ChangePasswordSerializer

class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        """
         An endpoint for logging in users
        
         URL: http://127.0.0.1:8000/api/login
         POST Request 
         Status Code: 200 
         Response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : generated-token,
            }
         Status Code: 404
         response = Serializer Errrors
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)

class UserRegistrationView(CreateAPIView):
    """
     An Endpoint for registering new users
    
     URL: http://127.0.0.1:8000/api/signup
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """
         POST Request 
        
         Status Code: 201 
         Response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered  successfully',
         }
         Status Code: 400
         response = Serializer Errors
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered  successfully',
        }
        
        return Response(response, status=status_code)

class ChangePasswordView(UpdateAPIView):
    """
     An Endpoint for changing password
    
     URL: http://127.0.0.1:8000/api/change_pass
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        """
         PUT Request 
        
         Status Code: 201 
         response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
         Status Code: 400
         response = Serializer Errors or old_password doesn't match
        """
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(DestroyAPIView):
    """
    An Endpoint for deleting the user from database
    URL: http://127.0.0.1:8000/api/delete_user
    """
    model = User
    permission_classes = (IsAuthenticated,)
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    def delete(self, request):
        """
        DELETE Request
        Status Code: 201 
        Response = N0_CONTENT
        Status Code: 400
        response = BAD_REQUEST
        """
        try:
            self.object = self.get_object()
            self.object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
