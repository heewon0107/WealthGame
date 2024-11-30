# 11-20 윤희준 퀘스트, 훈련장 쓸 장고 작성

from django.urls import path
from . import views



urlpatterns = [
    path('list/', views.quest_list, name='quest_list'),
]
