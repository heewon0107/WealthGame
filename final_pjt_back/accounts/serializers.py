# 11-18 신희원 회원가입 기능 추가
# 11-18 윤희준 로그인 기능 추가
from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nickname', 'age', 'assets', 'annual_income', 'desired_amount', 'desired_period', 'tier')

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'nickname', 'age', 'assets', 'annual_income', 'desired_amount', 'desired_period', 'tier')

    def validate_password(self, value):
        # 비밀번호 강도 검사를 위해 Django의 기본 비밀번호 검증기 사용
        validate_password(value)
        return value

    def create(self, validated_data):
        # 비밀번호를 해싱하여 사용자 객체 생성
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            nickname=validated_data.get('nickname', ''),
            age=validated_data.get('age', None),
            assets=validated_data.get('assets', None),
            annual_income=validated_data.get('annual_income', None),
            desired_amount=validated_data.get('desired_amount', None),
            desired_period=validated_data.get('desired_period', None),
            tier=validated_data.get('tier', '알거지')  # 기본값 '알거지'
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
