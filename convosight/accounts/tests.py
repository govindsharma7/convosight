from django.test import TestCase
from convosight.accounts.models import User


class UserTestCase(TestCase):
    """docstring for UserTestCase"""

    def setUp(self):
        User.objects.create_user(
            first_name='Govind',
            last_name='Sharma',
            email='govind@yopmail.com',
            password='123456789'
        )
        User.objects.create_user(
            first_name='Rahul',
            last_name='Sharma',
            email='rahul@yopmail.com',
            password='123456789'
        )

    def test_login(self):
        """docstring for user login"""

        user = User.objects.get(
            email="govind@yopmail.com")
        self.assertEqual(user.check_password('123456789'), True)
        user = User.objects.get(
            email="rahul@yopmail.com")
        self.assertEqual(user.check_password('1234567890'), False)
