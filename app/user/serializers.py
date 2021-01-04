from django.contrib.auth import get_user_model,authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    Serizlizer for the users object
    
    序列化用户对象
    """

    class Meta:
        model = get_user_model()
        fields =  ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self,validated_data):
        """
        Create a new user with encrypted password and return it
        
        创建新用户和加密的密码作为返回值
        """

        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a user, setting the password correctly and return it
        
        更新一个用户  ，并设置一个正确的密码并返回
        """
        password = validated_data.pop('password', None)
        user = super().update(instance,validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user




class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    """
    Generate token based on user information

    根据用户信息生成token
    """
    @classmethod
    def get_token(cls, user):
        token = super(TokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['name'] = user.name
        token['email'] = user.email

        return token