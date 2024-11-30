
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import JsonResponse
from django.conf import settings

from .models import Exchange
from .serializers import ExchangeSerializer

import requests

dollar_key = settings.DOLLAR_KEY

# 환율 정보 저장하기.
@api_view(['GET'])
def save_exchange(request):
    url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={dollar_key}&data=AP01'
    response = requests.get(url).json()
    
    # 받은 데이터를 처리하여 DB에 저장
    for li in response:
        result = li.get('result')
        cur_unit = li.get('cur_unit')
        cur_nm = li.get('cur_nm')
        ttb = li.get('ttb', 0)
        ttb = 0 if ttb is None else ttb
        tts = li.get('tts', 0)
        tts = 0 if tts is None else tts

        # DB에 이미 저장된 데이터가 있는지 확인
        if Exchange.objects.filter(cur_unit=cur_unit, cur_nm=cur_nm, ttb=ttb, tts=ttb).exists():
            continue  # 이미 존재하면 저장하지 않음

        # DB에 새로운 데이터 저장
        save_data = {
            'result': result,
            'cur_unit': cur_unit,
            'cur_nm': cur_nm,
            'ttb': ttb,
            'tts': tts,
        }

        serializer = ExchangeSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    return JsonResponse({'message' : "외환 정보 저장 성공"})

# 오늘 환율 정보 불러오기
@api_view(['GET'])
def today_exchange(request):
    exchanges = Exchange.objects.all()

    # 환율 정보가 없으면 빈 리스트 반환
    if not exchanges:
        return Response({'message': '오늘 환율 정보가 없습니다.'}, status=404)

    # 직렬화하여 반환
    serializer = ExchangeSerializer(exchanges, many=True)
    return Response(serializer.data)
