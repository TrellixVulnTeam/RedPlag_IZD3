## @package UserProfile
# @brief Handles request to get and update User profile
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from backend.app.user.serializers import UserRegistrationSerializer, UserSerializer
from backend.app.profile.models import UserProfile

class UserProfileView(RetrieveAPIView):
    """
    API Endpoint to Fetch and Update the user profile
    URL: http://127.0.0.1:8000/api/profile
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        """
         Used to fetch profile info for a user
        
         GET Request 
         Status Code: 200 
         Response = 
        {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': {
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'phone_number': user_profile.phone_number,
                    'age': user_profile.age,
                    'gender': user_profile.gender,
                    }
               }
         Status Code: 404
         response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': Server Error Message
        }
        """
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': {
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'phone_number': user_profile.phone_number,
                    'age': user_profile.age,
                    'gender': user_profile.gender,
                    }
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)

    def put(self, request):
        """
         Used to Update profile info for a user
        
         PUT Request 
         Status Code: 200 
         Response = User_profile Serializer output
         Status Code: 404
         response = Serializer Errrors
        """
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)