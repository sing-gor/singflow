from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# TOKEN_URL = reverse('user:token')
TOKEN_URL = reverse('token_obtain_pair')
CREATE_USER_URL = reverse('user:create')
ME_URL = reverse('user:me')

def create_user(**param):
    return get_user_model().objects.create_user(**param)




class PublicUserApiTests(TestCase):
    """
    Test the usersApi (public)
    检查用户Api
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
        Test creating user with valid payload is successful
        检查 创建用户的验证载体是否成功
        """

        payload = {
            'email': 'test@wongyusing.com',
            'password': 'testpassword',
            'name': 'testUsername'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """
        Test creating user that already exists fails
        检查 创建用户错误时，状态吗是否正确
        """
        payload = {'email': 'test@wongyusing.com', 'password': 'testpassword'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Test that the password must be more than 8 characters
        
        检查用户密码字段是否小于 8个字符
        """
        payload = {'email': 'test2@wongyusing.com', 'password': '11'}
        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """
        Test tha a token is created for the user
        
        检查用户token创建是否正常
        """
        payload = {'email': 'test@wongyusing.com', 'password': 'testpassword'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL,payload)

        self.assertIn('access',res.data)
        self.assertIn('refresh',res.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_token_invalid_credentials(self):
        """
        Test that token is not created if invalid credentials are given
        
        检查 当用户使用无效凭据时 是否会创建token
        """
        payload = {'email': 'test@wongyusing.com', 'password': 'false_testpassword'}
    
        res = self.client.post(TOKEN_URL, payload)


        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_no_user(self):
        """
        Test that token is not created if user does not exist
        
        检查 如果用户不存在 是否创建token
        """
        payload = {'email': 'test@wongyusing.com', 'password': 'testpassword'}
        res = self.client.post(TOKEN_URL, payload)
 
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_token_missing_filed(self):
        """
        Test that email and password are required
        
        检查当用户没有提交凭据时 是否会创建token
        """
        payload = {'email': 'tes', 'password': ''}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_retrieve_user_unauthorized(self):
        """
        Test that authentication is required for users
        
        检查用户是否需要验证信息
        """

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


    

class PrivateUserApiTests(TestCase):
    """
    Test Api requests that require authentication
    
    检查 APi 是否需要验证
    """

    def setUp(self):
        self.user = create_user(
            email='test@wongyusing.com',
            password='testpassword',
            name='testUsername'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    def test_retrieve_profile_success(self):
        """
        Test retrieving profile for logged in used
        
        检查已登入用户的的信息是否匹配
        """

        res = self.client.get(ME_URL)
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })
        
    def test_post_me_not_allowed(self):
        """
        Test that POST is not allowed on the me url
        
        检查 用户界面是否允许POST请求
        """
        res = self.client.post(ME_URL,{})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_updata_user_profile(self):
        """
        Test updating the user profile for authenticated user
        
        检查 已登入的用户，是否能更改个人信息
        """

        payload = {'name': 'Sing', 'password': 'newpassword4565'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)


        
