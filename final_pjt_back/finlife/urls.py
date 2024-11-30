from django.urls import path
from . import views

app_name = "finlifes"

urlpatterns = [
    path('save-deposit-products/', views.save_deposit_products, name='save'),
    path('deposit-products/', views.deposit_product, name='deposit'),
    path('deposit_product_detail/<str:fin_prdt_cd>/', views.deposit_product_detail, name='detail'),
    path('deposit-products-options/<str:fin_prdt_cd>/', views.deposit_product_options, name='detail'),
    path('deposit-products/top-rate/', views.top_rate, name='top_rate'),
    path('recommend_upload/', views.recommend_upload), # 11-18 신희원/ 예적금 데이터 불러오기
    path('id_to_deposit/', views.id_to_deposit),
    path('update_intr/', views.updata_intr) # 11-25 신희원 / 어드민 금리 수정 기능.
]
