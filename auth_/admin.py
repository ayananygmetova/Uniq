from django.contrib import admin

# Register your models here.
from auth_.models import MainUser

admin.site.register(MainUser)