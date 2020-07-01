from django.utils import timezone, translation
from django.utils.translation import gettext, activate
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.exceptions import CommonException
from utils.messages import (CONFIRM_EMAIL,
                            SUCCESS_REGISTER,
                            PASSWORD_CHANGED,
                            USER_DETAILS_CHANGED,
                            RESET_LINK_SENT,
                            ACCOUNT_EXIST)
from auth_.token import get_token
from auth_.models import MainUser
from auth_.serializers import MainUserSerializer, ChangePasswordSerializer, ChangeDetailsSerializer, RegistrationSerializer
from utils import messages, codes

USER = 'USER'


class SignUpView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        return MainUser.objects.get(email=self.request.data.get('email'))

    def post(self, request):
        queryset = self.get_queryset()
        if queryset:
            cur_language = translation.get_language()

            return Response({gettext(ACCOUNT_EXIST)},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer_class = RegistrationSerializer(data={"email": self.request.data.get('email'),
                                                        "password": self.request.data.get('password'),
                                                        "full_name": self.request.data.get('full_name')})
        serializer_class.is_valid()
        serializer_class.save()
        return Response(serializer_class.data,
                        status=status.HTTP_200_OK)


class LoginView(viewsets.ViewSet):
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        print(email, password)
        if email is None or password is None:
            raise CommonException(detail=gettext(messages.NO_CREDENTIALS),
                                  code=codes.NO_CREDENTIALS)
        try:
            user = MainUser.objects.get(email=email)
            if not user.check_password(password):
                raise CommonException(detail=gettext(messages.WRONG_EMAIL_OR_PASSWORD),
                                      code=codes.WRONG_EMAIL_OR_PASSWORD)
        except MainUser.DoesNotExist:
            raise CommonException(detail={gettext(messages.EMAIL_DOESNT_EXIST)},
                                  code=codes.EMAIL_DOESNT_EXIST)
        token = get_token(user)
        if user.role == USER:
            serializer = MainUserSerializer(user)
            return Response({'token': token, 'user': serializer.data},
                            status=status.HTTP_200_OK)


class ChangePassword(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        serializer = ChangePasswordSerializer(data=self.request.data,
                                              context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.change_password()
        return Response({gettext(PASSWORD_CHANGED)},
                        status=status.HTTP_200_OK)


class ChangeDetails(generics.UpdateAPIView):
    serializer_class = ChangeDetailsSerializer


    def put(self, request):
        serializer = ChangeDetailsSerializer(data=request.data,
                                             context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.change_details()
        user = MainUserSerializer(self.request.user)
        return Response((gettext(USER_DETAILS_CHANGED),
                            user.data),
                            status=status.HTTP_200_OK)
