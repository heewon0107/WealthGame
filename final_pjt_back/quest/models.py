# 11-20 윤희준 퀘스트, 훈련장 쓸 장고 작성

from django.db import models

# Create your models here.
class QuestCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Quest(models.Model):
        category = models.ForeignKey(QuestCategory ,related_name='quests', on_delete=models.CASCADE)
        question = models.TextField()
        answer = models.TextField()
        choices = models.TextField(blank=True, null=True) # 객관식의 경우 저장 해놓는 필드

        def __str__(self):
            return self.question
         
    
