from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import response, decorators, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserCreateSerializer

User = get_user_model()

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def registration(request):
    """User Registration View

    EndPoint -- http://localhost:8000/api/jwtauth/register/

  
    Input  -- ->
                {
                    "username":"Test_user_free_",
                    "email":"freee@gmail.com",
                    "password":"Secret@1234",
                    "password2":"Secret@1234",
                    "account_type":"free"
                }

                
    Output --  ->

                {
                "message": "user registered succesfully"
                }
    
    """
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)        
    user = serializer.save()
    
    res = {
       
        "message":"user registered succesfully"
    }
    return response.Response(res, status.HTTP_201_CREATED)
