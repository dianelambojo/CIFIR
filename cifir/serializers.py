from django.contrib.auth import get_user_model
from rest_framework import serializers


from .models import *


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password',
                  'first_name', 'last_name', 'key')
        write_only_fields = ('password')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active',)

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ['id']


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'title', 'cover', 'file', 'user', 'book_author']


class CollectionSerializer(serializers.ModelSerializer):

    #user = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Collection
        fields = ['id', 'name', 'book', 'user', 'isDeleted']
