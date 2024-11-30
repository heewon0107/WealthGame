from django.db import models
from django.contrib.auth import get_user_model
from finlife.models import DepositProducts

# Create your models here.
# 11-21 신희원 댓글 기능 모델 추가.
class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # 댓글 작성자 (로그인된 사용자)
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)  # 댓글이 달린 상품
    content = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 댓글 작성 시간
    tier = models.CharField(max_length=20, default='알거지') 