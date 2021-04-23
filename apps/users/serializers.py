import json

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'password')


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'password')


class AuthenticateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50, read_only=True)
    last_name = serializers.CharField(max_length=50, read_only=True)
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(max_length=50)
    token = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        # get user from models
        try:
            user_obj = User.objects.get(username=validated_data['username'])
        except User.DoesNotExist as error:
            raise User.MultipleObjectsReturned('User with this username not exists.') from error

        # compare passwords
        if not user_obj.check_password(validated_data['password']):
            raise ObjectDoesNotExist('Password and email no match.')
        user_serialized = UserSerializer(user_obj).data

        # try create token to auth, if exists, delete and create a new
        try:
            Token.objects.get(user=user_obj).delete()
        except Token.DoesNotExist:
            pass
        token = Token.objects.create(user=user_obj)
        user_serialized['token'] = token.key
        return user_serialized
