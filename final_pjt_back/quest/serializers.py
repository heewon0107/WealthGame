# 11-20 윤희준 퀘스트, 훈련장 쓸 장고 작성

from rest_framework import serializers
from quest.models import Quest, QuestCategory
class QuestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestCategory
        fields = ['id', 'name']

class QuestSerializer(serializers.ModelSerializer):
    category = QuestCategorySerializer()

    class Meta:
        model = Quest
        fields = ['id', 'category', 'question', 'answer', 'choices']