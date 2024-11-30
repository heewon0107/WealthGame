from django.db import models
from django.contrib.auth import get_user_model
from finlife.models import DepositProducts  # 상품 모델을 가져옵니다.

class Bucket(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='buckets')  # 유저와 연결
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name='buckets')  # 상품과 연결

    class Meta:
        unique_together = ('user', 'product')  # 같은 유저가 같은 상품을 중복 담을 수 없도록 설정