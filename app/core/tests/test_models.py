from django.test import TestCase

from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """
    Test Models

    检查模型
    """

    def test_create_user_with_email_successful(self):
        """
        test creating a new user with an email if successful 
        
        检查 使用email创建的用户 是否成功
        """
        email = 'test@wongyusing.com'
        password = 'wongyusing'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_email_normailzed(self):
        """
        Test the email for a new is normailzed
        检查email 字段是否又做归一处理判断
        """

        email = 'test@WONGYUSING.COM'
        user = get_user_model().objects.create_user(
            email=email,
            password='wongyusing'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_mail(self):
        """
        Test creating user with no email rails error
        检查 当用户没有填写email字段时，是否显示 参数验证错误
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                None,
                password='wongyusing'
            )

    def test_create_super_user(self):
        """
        Test creating an super user
        检查 创建超级用户时 是否运行正常
        """
        user = get_user_model().objects.create_superuser(
            email="admin@wongyusing.com",
            password='wongyusing'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
