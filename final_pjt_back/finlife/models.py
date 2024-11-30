from django.db import models
# Create your models here.

class DepositProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True) # 상품 코드
    kor_co_nm = models.TextField()              # 은행 이름
    fin_prdt_nm = models.TextField()            # 상품 이름
    etc_note = models.TextField()               # 특이사항
    join_deny = models.IntegerField()           # 가입 제한
    join_member = models.TextField()            # 가입 대상
    join_way = models.TextField()               # 가입 방법
    spcl_cnd = models.TextField()               # 우대 조건
    dcls_month = models.CharField(max_length=6)             # 공시 제출월

class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts,on_delete=models.CASCADE)
    fin_prdt_cd = models.TextField()            # 상품 코드
    intr_rate_type_nm=models.CharField(max_length=100)  # 저축 금리 유형명
    intr_rate = models.FloatField()             # 저축 금리
    intr_rate2 = models.FloatField()            # 최고 우대금리 
    save_trm = models.IntegerField()            # 저축 기간
