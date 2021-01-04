from django.test import TestCase, Client

from django.contrib.auth import get_user_model

from django.urls import reverse


class AdminSiteTests(TestCase):
    """
    站点后端 测试
    """
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@wongyusing.com',
            password='wongyusing'
        )

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@wongyusing.com',
            password='wongyusing',
            name='Test User full name'
        )

    def test_users_listed(self):
        """
        Test that users are listed on user page
        检查用户是否在用户列表中
        """
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)


    def test_user_change_page(self):
        """
        Test that the user page work
        检查用户界面是否工作
        """

        url = reverse('admin:core_user_change', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
