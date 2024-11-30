from django.shortcuts import render

# 11-18 신희원 회원가입 기능 추가
# 11-18 윤희준 로그인, 로그아웃 기능 추가
# 11-19 윤희준 로그인 기능 수정

# Create your views here.
# accounts/views.py
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserCreateSerializer, UserLoginSerializer, UserSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import User

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# 11-21 윤희준 프로필 조회, 수정 뷰 작성
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 11-21 윤희준 , 티어 수정위해 추가
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_tier(request):
    user = request.user
    new_tier = request.data.get('tier')
    user.tier = new_tier
    user.save()
    return Response({'success': True})

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # 사용자 생성
            return Response({"message": "회원가입 성공", "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 회원 탈퇴
@api_view(['DELETE'])
def delete_account(request):
    if request.method == 'DELETE':
        user = request.user  # 현재 로그인한 사용자 정보
        user.delete()  # 사용자 삭제
        return Response({"message": "회원 탈퇴 완료"}, status=status.HTTP_204_NO_CONTENT)

# 로그인
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            # email로 user 찾기
            try:
                user = User.objects.get(email=email)
                # check_password로 비밀번호 확인
                if user.check_password(password):
                    # 로그인 성공
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({
                        "message": "로그인 성공",
                        "token": token.key,
                        "user_id": user.id,
                        "is_superuser": user.is_superuser,
                        "userTier": user.tier
                    }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                pass
                
            return Response({
                "error": "이메일 또는 비밀번호가 잘못되었습니다."
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그아웃
@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        if request.auth:
            # request.auth.delete()  # 토큰 삭제
            return Response({"message": "로그아웃 성공"}, status=status.HTTP_200_OK)
        return Response({"error": "로그인 상태가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)


from bucket.models import Bucket
from finlife.models import DepositProducts
from finlife.serializers import DepositProductsSerializer
# 11-24 신희원 나와 비슷한 유저 조회
@api_view(['GET'])
def same(request, category):
    if category == '나이':
        my_age_group = request.user.age // 10
        users = User.objects.filter(age__gte = my_age_group * 10, age__lt=(my_age_group + 1) * 10)

    elif category == '자산':
        # 자산 필터링
        assets = int(request.GET.get('assets', 0))  # 자산 값 받아오기
        
        # 자산 범위 구간 설정
        if assets <= 10000000:
            min_assets = 1000000
            max_assets = 10000000  # 100만원 이상 1000만원 이하
        elif 10000000 < assets <= 20000000:
            min_assets = 10000000
            max_assets = 20000000  # 1000만원 이상 2000만원 이하
        elif 20000000 < assets <= 50000000:
            min_assets = 20000000
            max_assets = 50000000  # 2000만원 이상 5000만원 이하
        else:
            min_assets = 50000000
            max_assets = 1000000000  # 5000만원 이상, 최대 금액은 10억

        # 자산 범위에 맞는 사용자 필터링
        users = User.objects.filter(assets__gte=min_assets, assets__lte=max_assets)

    # 연간 수입 필터링
    elif category == '수입':
        income = int(request.GET.get('income', 0))  # 연간 수입 값 받아오기
        
        # 수입 범위 구간 설정
        if income <= 10000000:
            min_income = 1000000
            max_income = 10000000  # 100만원 이상 1000만원 이하
        elif 10000000 < income <= 30000000:
            min_income = 10000000
            max_income = 30000000  # 1000만원 이상 3000만원 이하
        elif 30000000 < income <= 50000000:
            min_income = 30000000
            max_income = 50000000  # 3000만원 이상 5000만원 이하
        else:
            min_income = 50000000
            max_income = 100000000  # 5000만원 이상, 최대 1억원

        # 수입 범위에 맞는 사용자 필터링
        users = User.objects.filter(annual_income__gte=min_income, annual_income__lte=max_income)
    
    # 투자 희망금액 필터링
    elif category == '금액':
        desired_amount = int(request.GET.get('desired_amount', 0))  # 투자 희망금액 값 받아오기
        
        # 희망금액 범위 구간 설정
        if desired_amount <= 10000000:
            min_desired_amount = 1000000
            max_desired_amount = 10000000  # 100만원 이상 1000만원 이하
        elif 10000000 < desired_amount <= 20000000:
            min_desired_amount = 10000000
            max_desired_amount = 20000000  # 1000만원 이상 2000만원 이하
        elif 20000000 < desired_amount <= 50000000:
            min_desired_amount = 20000000
            max_desired_amount = 50000000  # 2000만원 이상 5000만원 이하
        else:
            min_desired_amount = 50000000
            max_desired_amount = 1000000000  # 5000만원 이상, 최대 금액은 10억

        # 희망금액 범위에 맞는 사용자 필터링
        users = User.objects.filter(desired_amount__gte=min_desired_amount, desired_amount__lte=max_desired_amount)

    # 투자 희망기간 필터링
    elif category == '기간':
        desired_period = int(request.GET.get('desired_period', 0))  # 투자 희망기간 값 받아오기
        
        # 기간 범위 구간 설정
        if desired_period <= 12:
            min_period = 1
            max_period = 12  # 1~12개월
        elif 13 <= desired_period <= 24:
            min_period = 13
            max_period = 24  # 13~24개월
        elif 25 <= desired_period <= 36:
            min_period = 25
            max_period = 36  # 25~36개월
        else:
            return Response({"error": "기간은 1~36개월 사이로 설정해야 합니다."})

        # 기간 범위에 맞는 사용자 필터링
        users = User.objects.filter(desired_period__gte=min_period, desired_period__lte=max_period)
    
    elif category == '티어':
        tier = request.user.tier
        # 티어에 맞는 사용자 필터링
        if tier == '이자사냥꾼':
            users = User.objects.filter(tier='이자사냥꾼')
        elif tier == '알거지':
            users = User.objects.filter(tier='알거지')
        elif tier == '화폐술사':
            users = User.objects.filter(tier='화폐술사')
        elif tier == '건물주':
            users = User.objects.filter(tier='건물주')
        elif tier == '집마스터':
            users = User.objects.filter(tier='집마스터')
        elif tier == '차트마스터':
            users = User.objects.filter(tier='차트마스터')
        else:
            return Response({"error": "Invalid tier. Choose one from '이자사냥꾼', '화폐술사', '건물주', '집마스터', '차트마스터'."})

    user_serializer = UserSerializer(users, many=True)
    
    product_ids = set()
    for user_data in user_serializer.data:
        user_id = user_data['id']
        bucket = Bucket.objects.filter(user_id=user_id)
        if bucket:
            for b in bucket:
                product_ids.add(b.product_id)

    deposit_products = DepositProducts.objects.filter(id__in=product_ids)
    deposit_product_serializer = DepositProductsSerializer(deposit_products, many=True)

    return Response(deposit_product_serializer.data)

# 11-24 신희원 랭킹 시스템 도입
@api_view(['GET'])
def ranking(request):
    # 티어 순서 정의
    tier_order = [
        '건물주', '차트마스터', '집마스터', '화폐술사', '이자사냥꾼', '알거지'
    ]

    # 최대 3명만 반환하기 위한 리스트
    user_data = []
    
    # 각 티어에서 최대 3명까지 추출
    for tier in tier_order:
        users = User.objects.filter(tier=tier).order_by('-assets')[:3]  # 'assets' 기준으로 내림차순 정렬
        for user in users:
            user_data.append({
                "username": user.username,
                "tier": user.tier,
                "assets": user.assets,
            })
        
        # user_data의 길이가 3명을 넘으면 종료
        if len(user_data) >= 3:
            break

    return Response({"ranking": user_data[:3]})  # 최대 3명만 반환