from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Recipe


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )
    required_languages = ('en', 'ru')


translator.register(Category, CategoryTranslationOptions)


class RecipeTranslationOptions(TranslationOptions):
    fields = ('name', 'ingredients', 'recipes', 'accessorizes', 'hint', 'category',
              'difficulty')
    required_languages = ('en', 'ru')


translator.register(Recipe, RecipeTranslationOptions)
