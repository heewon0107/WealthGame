# 11-18 신희원 회원가입 기능 url 생성.
# 11-18 윤희준 로그인, 로그아웃 기능 url 생성.
from django.urls import path
from . import views

urlpatterns = [
    # 11-21 윤희준 , 프로필 및 티어 추가
    path('profile_view/', views.profile_view),
    path('update_tier/', views.update_tier),
    # ---------------------------------------
    path('register/', views.register, name='register'),
    path('delete/', views.delete_account, name='delete_account'),
    path('login/', views.login, name='login'),         
    path('logout/', views.logout, name='logout'),  
    # ---------------------------------------
    # 11-24 신희원, 나와 비슷한 유저 정보 뽑기
    path('same/<str:category>/', views.same),
    # ---------------------------------------
    # 11-24 신희원, 티어 순위표 만들기
    path('ranking/', views.ranking)
]