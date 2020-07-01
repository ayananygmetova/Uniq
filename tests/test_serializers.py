from django.test import TestCase, RequestFactory
from django.utils.timezone import localtime
from model_mommy import mommy

from auth_.models import MainUser
from auth_.serializers import (
    MainUserSerializer,
    ChangePasswordSerializer,
    ChangeDetailsSerializer)
from utils.exceptions import CommonException
from utils import messages, codes



class BaseTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = MainUser.objects.create_user(
            email="test_email@gmail.com",
            password='test_password',
            full_name="test_full_name")
        cls.factory = RequestFactory()
        cls.request = cls.factory.post('/')
        cls.request.user = cls.user


class ChangePasswordSerializerTest(BaseTest):

    def test_change_password_serializer(self):
        data = {
            'password': 'test_password',
            'password1': 'testik12345',
            'password2': 'testik12345'
        }
        serializer = ChangePasswordSerializer(
            data=data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        self.assertEqual(data['password'],
                         serializer.data['password'])
        self.assertEqual(data['password1'],
                         serializer.data['password1'])
        self.assertEqual(data['password2'],
                         serializer.data['password2'])

    def test_validate_raise(self):
        data = {
            'password': 'test_password',
            'password1': 'testik12344',
            'password2': 'testik12345'
        }
        serializer = ChangePasswordSerializer(data=data, context={'request': self.request})
        with self.assertRaises(CommonException, msg='Неверный пароль'):
            serializer.is_valid(raise_exception=True)
        data['password'] = 'testik123'
        serializer2 = ChangePasswordSerializer(data=data, context={'request': self.request})
        with self.assertRaises(CommonException, msg='Пароли не совпадают'):
            serializer2.is_valid(raise_exception=True)

    def test_change_password(self):
        data = {
            'password': 'test_password',
            'password1': 'testik12345',
            'password2': 'testik12345'
        }
        serializer = ChangePasswordSerializer(
            data=data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.change_password()
        self.assertTrue(self.request.user.check_password(data['password1']))


class ChangeDetailsSerializerTest(BaseTest):

    def test_change_details_serializer(self):
        data = {
            'email': self.user.email,
            'full_name': 'Test Name'
        }
        serializer = ChangeDetailsSerializer(
            data=data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        self.assertEqual(data['email'], serializer.data['email'])
        self.assertEqual(data['full_name'], serializer.data['full_name'])

    def test_validate_raise(self):
        MainUser.objects.create(email='test2@gmail.com',
                                password="password")
        data = {
            'email': 'test2@gmail.com',
            'full_name': "Test Name"
        }
        serializer = ChangeDetailsSerializer(data=data, context={'request': self.request})
        with self.assertRaises(
                CommonException,
                msg='Такой email уже существует'):
            serializer.is_valid(raise_exception=True)

    def test_change_details_user(self):
        data = {
            'email': self.user.email,
            'full_name': "Test Name"
        }
        serializer = ChangeDetailsSerializer(
            data=data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.change_details()
        self.assertEqual(data['full_name'],
                         self.request.user.full_name)
