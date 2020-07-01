from django.test import TestCase, RequestFactory
from django.urls import reverse
from model_mommy import mommy

from rest_framework_jwt.utils import jwt_decode_handler

# Create your tests here.
from auth_.models import MainUser
from auth_.token import get_token
from core.models import Category
from core.views import CategoryListView

from auth_.views import LoginView

from core.models import Recipe

from core.views import RecipeListView

from core.views import RecipesOfCategory

from core.views import FavoriteView


class CategoryListViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.data = {
            'email': 'test@gmail.com',
            'password': 'test_password'
        }
        self.test_user = MainUser.objects.create_user(**self.data)
        for i in range(10):
            mommy.make(Category, name="test_name %s" % i)

    def test_is_authorized(self):
        auth_headers = {
            'HTTP_AUTHORIZATION': 'JWT ' + get_token(self.test_user)
        }
        request = self.factory.get(reverse('get_post_categories'), **auth_headers)
        resp = CategoryListView.as_view()(request)
        n = len(Category.objects.all())
        self.assertEqual(n, len(resp.data))

    def test_is_not_authorized(self):
        request = self.factory.get(reverse('get_post_categories'))
        response = CategoryListView.as_view()(request)
        self.assertEqual(response.status_code, 401)

    def test_get_categories(self):
        auth_headers = {
            'HTTP_AUTHORIZATION': 'JWT ' + get_token(self.test_user)
        }
        request = self.factory.get(reverse('get_post_categories'), **auth_headers)
        response = CategoryListView.as_view()(request)
        self.assertEqual(response.data[0]['name'], 'test_name 0')
        self.assertEqual(response.status_code, 200)

    def test_post_categories(self):
        auth_headers = {
            'HTTP_AUTHORIZATION': 'JWT ' + get_token(self.test_user)
        }
        test_review = {
            'name': 'test category'
        }
        request = self.factory.post(reverse('get_post_categories'), data=test_review, **auth_headers)
        response = CategoryListView.as_view()(request)
        self.assertEqual(response.status_code, 201)


class TokenGetTest(TestCase):

    def setUp(self):
        self.user = MainUser.objects.create_user(
            email='test@gmail.com', password='test_password')

    def test_get_token(self):
        response = get_token(self.user)
        decoded_payload = jwt_decode_handler(response)
        self.assertEqual(decoded_payload['username'], 'test@gmail.com')


class AuthenticationTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.data = {
            'email': 'test@gmail.com',
            'password': 'test_password'
        }
        self.test_user = MainUser.objects.create_user(**self.data)

    def test_login(self):
        request = self.factory.post('/login/', self.data)
        view = LoginView.as_view({'post': 'login'})
        response = view(request)
        decoded_payload = jwt_decode_handler(response.data['token'])
        self.assertEqual(decoded_payload['username'], self.data['email'])


class RecipeTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.data = {
            'email': 'test@gmail.com',
            'password': 'test_password'
        }
        self.test_user = MainUser.objects.create_user(**self.data)
        for i in range(10):
            Recipe.objects.create(name="test recipe %s" % i, ingredients='test ingredients %s' % i,
                                  recipes='recipes %s' % i,
                                  accessorizes='test accessorizes %s' % i, hint='test hint %s' % i)

    def test_is_authorized(self):
        auth_headers = {
            'HTTP_AUTHORIZATION': 'JWT ' + get_token(self.test_user)
        }
        request = self.factory.get(reverse('get_post_recipes'), **auth_headers)
        resp = RecipeListView.as_view()(request)
        n = len(Recipe.objects.all())
        self.assertEqual(n, len(resp.data))

    def test_is_not_authorized(self):
        request = self.factory.get(reverse('get_post_recipes'))
        response = RecipeListView.as_view()(request)
        self.assertEqual(response.status_code, 401)

    def test_get_recipes(self):
        auth_headers = {
            'HTTP_AUTHORIZATION': 'JWT ' + get_token(self.test_user)
        }
        request = self.factory.get(reverse('get_post_recipes'), **auth_headers)
        response = RecipeListView.as_view()(request)
        self.assertEqual(response.data[0]['name'], 'test recipe 0')
        self.assertEqual(len(response.data), len(Recipe.objects.all()))
        self.assertEqual(response.status_code, 200)


class RecipesOfCategoryTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.data = {
            'email': 'test@gmail.com',
            'password': 'test_password'
        }
        self.test_user = MainUser.objects.create_user(**self.data)
        categories = []
        for i in range(5):
            categories.append(Category.objects.create(name="test category %s" % i))
        for i in range(10):
            Recipe.objects.create(name="test recipe %s" % i, ingredients='test ingredients %s' % i,
                                  recipes='recipes %s' % i,
                                  accessorizes='test accessorizes %s' % i, hint='test hint %s' % i,
                                  category=categories[i // 2])

    # def test_recipe_of_category(self):
    #     auth_headers = {
    #         'HTTP_AUTHORIZATION': 'JWT ' + get_token(self.test_user)
    #     }
    #     for i in range(10):
    #         request = self.factory.get('/categories/%s' % i, **auth_headers)
    #         response = RecipesOfCategory.as_view()(request)
    #         self.assertEqual(response.objects, 'test recipe %s' % i)
    #         print(response.objects.all())
    #         self.assertEqual(len(response), 2)


class Favorites(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.data = {
            'email': 'test@gmail.com',
            'password': 'test_password'
        }
        self.test_user = MainUser.objects.create_user(**self.data)
        self.recipes = []
        for i in range(10):
            self.recipes.append(Recipe.objects.create(name="test recipe %s" % i, ingredients='test ingredients %s' % i,
                                                      recipes='recipes %s' % i,
                                                      accessorizes='test accessorizes %s' % i, hint='test hint %s' % i))
        self.test_user.favorite.add(self.recipes[0])
        self.test_user.favorite.add(self.recipes[1])

    def test_favorites_list(self):
        auth_headers = {
            'HTTP_AUTHORIZATION': 'JWT ' + get_token(self.test_user)
        }
        request = self.factory.get(reverse('favorites'), **auth_headers)
        response = FavoriteView.as_view({'get': 'list'})(request)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0], self.recipes[0])
