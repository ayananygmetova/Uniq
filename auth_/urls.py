"""
This file contains url requests of auth_ app.
Here you can acquainted with path needed to access certain data.
"""
from django.urls import path

from auth_ import views

# sign_up = views.SignUpView.as_view({
#     'post': 'create'})

login = views.LoginView.as_view({
    'post': 'login'})



urlpatterns = [
    path('signup/', views.SignUpView.as_view()),
    path('login/', login, name='login'),
    path('change_password/', views.ChangePassword.as_view()),
    path('change_details/', views.ChangeDetails.as_view())
]
