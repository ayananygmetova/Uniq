from rest_framework import serializers

from auth_.models import MainUser
from utils.exceptions import CommonException
from django.contrib.auth.hashers import make_password
from utils import messages, codes


class MainUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = '__all__'


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    full_name = serializers.CharField()

    def save(self):
        MainUser.objects.create_user(self.validated_data['email'],
                                     self.validated_data['password'],
                                     self.validated_data['full_name'])


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100)
    password1 = serializers.CharField(max_length=100)
    password2 = serializers.CharField(max_length=100)

    def validate(self, attrs):
        if not self.context['request'].user.check_password(attrs['password']):
            raise CommonException(detail=messages.WRONG_PASSWORD, code=codes.WRONG_PASSWORD)
        if attrs['password1'] != attrs['password2']:
            raise CommonException(detail=messages.PASSWORDS_NOT_SAME,
                                  code=codes.PASSWORDS_NOT_SAME)
        return attrs

    def change_password(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['password1'])
        user.save()


class ChangeDetailsSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100)

    def validate(self, attrs):
        if self.context['request'].user.email != attrs['email']:
            if MainUser.objects.filter(email=attrs['email']).exists():
                raise CommonException(detail=messages.ALREADY_EXIST,
                                      code=codes.ALREADY_EXIST)
        return attrs

    def change_details(self):
        user = self.context['request'].user
        user.full_name = self.validated_data['full_name']
        user.email = self.validated_data['email']
        user.save()
