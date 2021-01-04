from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer,TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView
class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the system
    
    在系统中创建一个新用户
    """

    serializer_class = UserSerializer



class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Manage the authenticated user
    
    用户的信息界面，即ProFile界面
    """

    serializer_class = UserSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """
        Retrieve and return authentication user
        
        取得登入用户的信息
        """

        return self.request.user


class TokenObtainPairView(BaseTokenObtainPairView):
    """
    Generate token based on user information

    根据用户信息生成token
    """
    serializer_class = TokenObtainPairSerializer