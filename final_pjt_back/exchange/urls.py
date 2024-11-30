from django.urls import path
from . import views

app_name = "exchange"

urlpatterns = [
    path('save_exchange/', views.save_exchange),    # 환율 정보 저장
    path('today_exchange/', views.today_exchange),  # 오늘 환율
]
