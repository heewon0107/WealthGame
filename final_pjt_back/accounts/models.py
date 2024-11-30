from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# 11-18 신희원 회원가입 기능 추가.

class User(AbstractUser):
    # 추가적인 필드 생성.
    username = models.CharField(max_length=100, unique=True)  # 회원 아이디
    email = models.EmailField(unique=True)  # 이메일 (unique=True로 중복 방지)
    nickname = models.CharField(max_length=50)  # 닉네임
    password = models.CharField(max_length=255)  # 비밀번호 (상속받은 AbstractUser에서 이미 포함)
    age = models.IntegerField()  # 나이
    assets = models.DecimalField(max_digits=15, decimal_places=2)  # 자산
    annual_income = models.DecimalField(max_digits=15, decimal_places=2)  # 연간 수입
    desired_amount = models.DecimalField(max_digits=15, decimal_places=2)  # 목표 금액
    desired_period = models.IntegerField()  # 목표 기간 (개월 수)
    tier = models.CharField(max_length=20, default='알거지',null=True)  # 기본값을 '알거지'로 설정
    # 11-19 윤희준 추가
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []