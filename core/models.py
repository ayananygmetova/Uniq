from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from auth_.models import MainUser


class Category(models.Model):
    name = models.CharField(max_length=150)

    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }



class Recipe(models.Model):
    name = models.CharField(max_length=10000)
    image = models.CharField(max_length=10000, blank=True, null=True)
    stars = models.FloatField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True,
                                null=True)
    ingredients = models.TextField(blank=True, null=True)
    time = models.CharField(max_length=50, blank=True, null=True)
    recipes = models.TextField()
    accessorizes = models.TextField()
    hint = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='food', blank=True, null=True)
    model = models.CharField(max_length=10000, blank=True, null=True)
    difficulty = models.CharField(max_length=10000, blank=True, null=True)
    favorite = models.ManyToManyField(MainUser, blank=True, related_name="favorite")
    shared = models.ManyToManyField(MainUser, blank=True, related_name="shared")
    cooked = models.ManyToManyField(MainUser, blank=True, related_name="cooked")

    def __str__(self):
        return str({
            'name': self.name,
            'ingredients': self.ingredients,
            'recipes': self.recipes,
            'accessorizes': self.accessorizes,
            'hint': self.hint,
        })
