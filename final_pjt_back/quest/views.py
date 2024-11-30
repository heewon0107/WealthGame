# 11-20 윤희준 퀘스트, 훈련장 쓸 장고 작성

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import Quest
from .serializers import QuestSerializer
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404,get_list_or_404



@api_view(['GET'])
def quest_list(request):
    quests = get_list_or_404(Quest)
    serializer = QuestSerializer(quests, many=True)
    return Response(serializer.data)

