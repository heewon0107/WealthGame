from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from django.http import JsonResponse
import requests

# Create your views here.
@api_view(['GET'])
def news(request):
    keyword = request.GET.get('keyword', '')
    url = "https://api-v2.deepsearch.com/v1/articles"    # API 호출 URL과 파라미터 설정
    params = {
        "keyword": keyword,
        "api_key": settings.NEWS_KEY,
    }
    response = requests.get(url, params=params)    # 딥서치 API 호출
    if response.status_code == 200:    # API 응답 반환
        return JsonResponse(response.json(), safe=False, status=200)
    return JsonResponse({"error": "Failed to fetch data from DeepSearch API"}, status=response.status_code)