from django.urls import path
from . import views

app_name = "bucket"

urlpatterns = [
    path('', views.bucket),    # 장바구니 담기, 빼기, 조회 기능
    path('have/', views.check_if_product_in_bucket),
]
