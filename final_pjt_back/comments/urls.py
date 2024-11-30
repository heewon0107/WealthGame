from django.urls import path
from . import views

urlpatterns = [
    path('api/products/<int:product_id>/comments/', views.get_comments, name='get_comments'),
    path('api/products/comments/', views.post_comment, name='post_comment'),
    path('api/comments/update/', views.update_comment),
    path('api/comments/delete/', views.delete_comment),
    # 로그인 여부 확인 엔드포인트
    path('api/check-authentication/', views.check_authentication, name='check_authentication'),
]