from rest_framework import serializers
from .models import User, UserActivity, LandingPage
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password',
                 'total_keystrokes', 'total_coins', 'current_streak')
        extra_kwargs = {
            'password': {'write_only': True},
            'total_keystrokes': {'read_only': True},
            'total_coins': {'read_only': True},
            'current_streak': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ('id', 'date', 'keystrokes', 'coins_earned', 'source_app')
        read_only_fields = ('id', 'date', 'coins_earned')

class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('total_keystrokes', 'total_coins', 'current_streak')
        read_only_fields = fields

class LandingPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPage
        fields = '__all__'