from django.db import models

import uuid
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError

ADMIN = 'ADMIN'
USER = 'USER'

ROLES = (
    (ADMIN, "Admin"),
    (USER, "User")
)
ACTIVATION_TIME = 10


class MainUserManager(BaseUserManager):
    def create_user(self, email, password, full_name=None):
        if not email:
            raise ValueError('User must have a email')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.is_moderator = True
        user.is_staff = True
        user.role = ADMIN
        user.save(using=self._db)
        return user


class MainUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    full_name = models.CharField(max_length=255, blank=True,
                                 null=True, verbose_name='Имя')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    email = models.EmailField(max_length=50, verbose_name='Почта',
                              unique=True, db_index=True)
    role = models.CharField(max_length=100, choices=ROLES, default=USER,
                            verbose_name="Роль")
    timestamp = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True,
                                    verbose_name='Активность')
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')
    objects = MainUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return '{}: {}'.format(self.full_name, self.email)
