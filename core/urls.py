from django.urls import path

from core.views import CategoryListView, RecipeListView, FavoriteListView, FavoriteView, CookedListView, CookedView, RecipesOfCategory

favorite_list = FavoriteListView.as_view({'get': 'list'})

favorite_detail = FavoriteView.as_view({
    'get': 'get',
    'delete': 'destroy',
    'post': 'add_to_favorites'})
cooked_list = CookedListView.as_view({'get': 'list'})

cooked_detail = CookedView.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
    'post': 'update'})

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name="get_post_categories"),
    path('recipes/', RecipeListView.as_view(), name="get_post_recipes"),
    path('categories/<int:pk>', RecipesOfCategory.as_view(), name="recipes_of_categories"),
    path('favorites/', favorite_list, name="favorites"),
    path('favorite/<int:pk>/', favorite_detail),
    path('cooked/', cooked_list),
    path('cooked/<int:pk>/', cooked_detail)

]