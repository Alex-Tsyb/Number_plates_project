from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm


class UserAuthenticationTest(TestCase):
    def test_register_view(self):
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)

        self.assertIsInstance(response.context['form'], RegisterForm)

    def test_register_success(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(reverse('users:signup'), data)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login_view(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

        self.assertIsInstance(response.context['form'], LoginForm)

    def test_login_success(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(reverse('users:login'), data)
        self.assertEqual(response.status_code, 302)

        self.assertIn('_auth_user_id', self.client.session)

    def test_logout(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.force_login(user)
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)

        self.assertNotIn('_auth_user_id', self.client.session)
