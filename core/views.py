from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from core.models import Category
from django.shortcuts import get_object_or_404
from core.serializers import CategorySerializer

from core.models import Recipe
from core.serializers import RecipeSerializer

from auth_.models import MainUser


class CategoryListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RecipeListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipesOfCategory(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeSerializer

    def get_queryset(self):
        category = Category.objects.get(id=self.kwargs.get('pk'))
        queryset = category.food.all()
        serializer = RecipeSerializer(queryset, many=True)
        return queryset


class FavoriteListView(viewsets.ViewSet):
    def list(self, request):
        user = MainUser.objects.get(email=self.request.user.email)
        queryset = user.favorite.all()
        serializer = RecipeSerializer(queryset, many=True)
        return Response(serializer.data)


class FavoriteView(viewsets.ViewSet):
    def get(self, request, pk=None):
        user = MainUser.objects.get(email=self.request.user.email)
        queryset = user.favorite.all()
        recipe = get_object_or_404(queryset, pk=pk)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        user = MainUser.objects.get(email=self.request.user.email)
        queryset = user.favorite.all()
        recipe = get_object_or_404(queryset, pk=pk)
        recipe.favorite.delete()
        return Response({'DELETED': True})

    def add_to_favorites(self, request, pk=None):
        user = MainUser.objects.get(email=self.request.user.email)
        recipe = Recipe.objects.get(id=pk)
        user.favorite.add(recipe)
        return Response({'ADDED': True})


class CookedListView(viewsets.ViewSet):
    def list(self, request):
        user = MainUser.objects.get(email=self.request.user.email)
        queryset = user.cooked.all()
        serializer = RecipeSerializer(queryset, many=True)
        return Response(serializer.data)


class CookedView(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        user = MainUser.objects.get(email=self.request.user.email)
        queryset = user.cooked.all()
        recipe = get_object_or_404(queryset, pk=pk)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        user = MainUser.objects.get(email=self.request.user.email)
        queryset = user.cooked.all()
        recipe = get_object_or_404(queryset, pk=pk)
        recipe.cooked.delete()
        return Response({'DELETED': True})

    def update(self, pk=None):
        user = MainUser.objects.get(email=self.request.user.email)
        recipe = Recipe.objects.get(id=pk)
        user.cooked.add(recipe)
        return Response({'ADDED': True})
