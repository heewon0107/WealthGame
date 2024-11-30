from django.shortcuts import render
from .models import DepositProducts, DepositOptions
from rest_framework.decorators import api_view
import requests
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from django.http import JsonResponse
from .serializers import DepositProductsSerializer, DepositOptionsSerializer
from django.shortcuts import get_object_or_404,get_list_or_404
from django.db.models import Max

from bucket.models import Bucket
from finlife.models import DepositProducts
# 11-18 신희원 예적금 데이터 불러오기

api_key = settings.API_KEY
# Create your views here.

# 예적금 상품 저장하기.
@api_view(['GET'])
def save_deposit_products(request):
    
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'

    savings_url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'


    response = requests.get(url).json()

    savings_response = requests.get(savings_url).json()

    # 정기 예금 상품 생성
    for li in response['result'].get('baseList'):
        
        fin_prdt_cd = li.get('fin_prdt_cd')
        kor_co_nm = li.get('kor_co_nm')
        fin_prdt_nm = li.get('fin_prdt_nm')
        etc_note = li.get('etc_note')
        join_deny = li.get('join_deny')
        join_member = li.get('join_member')
        join_way = li.get('join_way')
        spcl_cnd = li.get('spcl_cnd', "-1")
        dcls_month = li.get('dcls_month', "-1")

        # DB에 이미 저장되어 있는 지 중복 확인
        if DepositProducts.objects.filter(  
            fin_prdt_cd=fin_prdt_cd, 
            kor_co_nm=kor_co_nm, 
            fin_prdt_nm=fin_prdt_nm,
            etc_note=etc_note,
            join_deny=join_deny,
            join_member=join_member,
            join_way=join_way,
            spcl_cnd=spcl_cnd,
            dcls_month = dcls_month
            ).exists():
            continue

        # 3. "DB에 없다면" 저장한다.
        save_data = {
            'fin_prdt_cd':fin_prdt_cd, 
            'kor_co_nm':kor_co_nm, 
            'fin_prdt_nm':fin_prdt_nm,
            'etc_note':etc_note,
            'join_deny':join_deny,
            'join_member':join_member,
            'join_way':join_way,
            'spcl_cnd':spcl_cnd,
            'dcls_month':dcls_month
        }

        serializer = DepositProductsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    
    # 옵션 생성
    for li in response['result'].get('optionList'):
        fin_prdt_cd = li.get('fin_prdt_cd')
        intr_rate_type_nm = li.get('intr_rate_type_nm', '-1')
        intr_rate = li.get('intr_rate', -1)
        if intr_rate == None:
            intr_rate = -1
        intr_rate2 = li.get('intr_rate2', -1)
        save_trm = li.get('save_trm', -1)
        if save_trm in ['1', '3']: # 최소 3개월로 ㄱㄱ
            continue

        # DB에 이미 저장되어 있는 지 중복 확인
        if DepositOptions.objects.filter(  
            fin_prdt_cd=fin_prdt_cd, 
            intr_rate_type_nm=intr_rate_type_nm, 
            intr_rate=intr_rate,
            intr_rate2=intr_rate2,
            save_trm=save_trm
        
            ).exists():
            continue

        # 3. "DB에 없다면" 저장한다.
        save_data = {
            'fin_prdt_cd':fin_prdt_cd, 
            'intr_rate_type_nm':intr_rate_type_nm, 
            'intr_rate':intr_rate,
            'intr_rate2':intr_rate2,
            'save_trm':save_trm
        }
        product = get_object_or_404(DepositProducts, fin_prdt_cd=fin_prdt_cd)
        serializer = DepositOptionsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(product=product)
    
    # 정기 적품 상품 생성
    for li in savings_response['result'].get('baseList'):
        
        fin_prdt_cd = li.get('fin_prdt_cd')
        kor_co_nm = li.get('kor_co_nm')
        fin_prdt_nm = li.get('fin_prdt_nm')
        etc_note = li.get('etc_note')
        join_deny = li.get('join_deny')
        join_member = li.get('join_member')
        join_way = li.get('join_way')
        spcl_cnd = li.get('spcl_cnd', "-1")
        dcls_month = li.get('dcls_month', "-1")

        # DB에 이미 저장되어 있는 지 중복 확인
        if DepositProducts.objects.filter(  
            fin_prdt_cd=fin_prdt_cd, 
            kor_co_nm=kor_co_nm, 
            fin_prdt_nm=fin_prdt_nm,
            etc_note=etc_note,
            join_deny=join_deny,
            join_member=join_member,
            join_way=join_way,
            spcl_cnd=spcl_cnd,
            dcls_month = dcls_month
            ).exists():
            continue

        # 3. "DB에 없다면" 저장한다.
        save_data = {
            'fin_prdt_cd':fin_prdt_cd, 
            'kor_co_nm':kor_co_nm, 
            'fin_prdt_nm':fin_prdt_nm,
            'etc_note':etc_note,
            'join_deny':join_deny,
            'join_member':join_member,
            'join_way':join_way,
            'spcl_cnd':spcl_cnd,
            'dcls_month':dcls_month
        }

        serializer = DepositProductsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    
    # 옵션 생성
    for li in savings_response['result'].get('optionList'):
        
        fin_prdt_cd = li.get('fin_prdt_cd')
        intr_rate_type_nm = li.get('intr_rate_type_nm', '-1')
        intr_rate = li.get('intr_rate', -1)
        if intr_rate == None:
            intr_rate = -1
        intr_rate2 = li.get('intr_rate2', -1)
        save_trm = li.get('save_trm', -1)
        if save_trm in ['1', '3']: # 최소 6개월로 ㄱㄱ
            continue

        # DB에 이미 저장되어 있는 지 중복 확인
        if DepositOptions.objects.filter(  
            fin_prdt_cd=fin_prdt_cd, 
            intr_rate_type_nm=intr_rate_type_nm, 
            intr_rate=intr_rate,
            intr_rate2=intr_rate2,
            save_trm=save_trm
        
            ).exists():
            continue

        # 3. "DB에 없다면" 저장한다.
        save_data = {
            'fin_prdt_cd':fin_prdt_cd, 
            'intr_rate_type_nm':intr_rate_type_nm, 
            'intr_rate':intr_rate,
            'intr_rate2':intr_rate2,
            'save_trm':save_trm
        }
        product = get_object_or_404(DepositProducts, fin_prdt_cd=fin_prdt_cd)
        serializer = DepositOptionsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(product=product)

    product = DepositProducts.objects.all()
    for pr in product:
        if not DepositOptions.objects.filter(fin_prdt_cd=pr.fin_prdt_cd):
            pr.delete()
            

    return JsonResponse({'message' : "저장 성공"})

# 예적금 상품 조회하기.
@api_view(['GET']) 
def deposit_product_detail(request, fin_prdt_cd):
    detail = get_object_or_404(DepositProducts, fin_prdt_cd=fin_prdt_cd)
    serializer = DepositProductsSerializer(detail)
    return Response(serializer.data)

# 예적금 상품 옵션 조회하기.
@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    options = get_list_or_404(DepositOptions, fin_prdt_cd=fin_prdt_cd)
    serializer = DepositOptionsSerializer(options, many=True)
    return Response(serializer.data)

# 11-25 신희원 email 보내는 로직 구현
from django.core.mail import send_mail

def send_email(fin_prdt_cd, last_option, next_option):
    product = get_object_or_404(DepositProducts, fin_prdt_cd=fin_prdt_cd)
    buckets = get_list_or_404(Bucket, product_id=product)
    bank_name = product.kor_co_nm
    product_name = product.fin_prdt_nm
    subject = 'WEALTH GAME의 금리가 변경되었습니다!!!'
    message = f'금리가 변경되었습니다. 자세한 사항을 확인하세요.\n\n{bank_name}의 {product_name} 상품 변경 내용.\n금리 : {last_option["intr_rate"]} > {next_option["intr_rate"]}\n최대 우대금리 : {last_option["intr_rate2"]} > {next_option["intr_rate2"]}\n가입 기간 : {next_option["save_trm"]}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = []  # 수신자 이메일 리스트

    # 받은 아이템 코드가 있는 장바구니 조회
    # 장바구니 순회하면서 유저 이메일 배열에 추가.
    for bucket in buckets:
        recipient_list.append(bucket.user.email)

    if recipient_list:  # 유효한 이메일 주소가 있다면
        try:
            print(f"Sending email to: {recipient_list}")
            send_mail(subject, message, from_email, recipient_list)
            print("Email sent successfully")
        except Exception as e:
            print(f"Error sending email: {e}")
    else:
        print("No valid emails found in the recipient list.")

@api_view(['POST'])
def updata_intr(request):
    # 슈퍼유저아니면 탈락
    if not request.user.is_superuser:
        return Response({'message' : "슈퍼유저만 금리 정보 수정 가능."})
    try:
        # 요청에서 option_id, 금리, 최고 우대금리 가져오기
        option_id = request.GET.get('option_id')
        intr_rate = request.GET.get('intr_rate')
        intr_rate2 = request.GET.get('intr_rate2')
        # option_id가 없으면 400 Bad Request 응답
        if not option_id or intr_rate is None or intr_rate2 is None:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        # DepositOptions에서 option_id에 해당하는 옵션 찾기
        option = DepositOptions.objects.get(id=option_id)
        last_option = {
            'intr_rate': option.intr_rate,
            'intr_rate2': option.intr_rate2
        }

        # 금리 수정
        option.intr_rate = intr_rate
        option.intr_rate2 = intr_rate2
        next_option = {
            'intr_rate': option.intr_rate,
            'intr_rate2': option.intr_rate2,
            'save_trm': option.save_trm
        }
        option.save()  # 데이터베이스에 저장
        serializer = DepositOptionsSerializer(option)

        # 여기서 이메일 발송할 것임.
        send_email(option.fin_prdt_cd, last_option, next_option)

        # 성공적으로 수정된 옵션을 반환
        return Response({'message': '금리 정보가 수정되었습니다.'}, status=status.HTTP_200_OK)


    except DepositOptions.DoesNotExist:
        return Response({'error': 'Option not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# 예적금 상품 전체 조회하기
@api_view(['GET','POST'])
def deposit_product(request):
    if request.method=='GET':
        product = get_list_or_404(DepositProducts)
        serializer = DepositProductsSerializer(product,many=True)
        return Response(serializer.data)
    if request.method=='POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

# 예적금 상품 
@api_view(['GET'])
def top_rate(request):

    if request.method=='GET':
        max_intr_rate2 = DepositOptions.objects.aggregate(intr_rate2=Max('intr_rate2'))['intr_rate2']
        option=get_object_or_404(DepositOptions,intr_rate2=max_intr_rate2)

        product=get_object_or_404(DepositProducts,fin_prdt_cd=option.fin_prdt_cd)

        serializer1 = DepositOptionsSerializer(option)
        serializer2 = DepositProductsSerializer(product)
        return Response({'deposit_product':serializer2.data,'option':[serializer1.data]})
    
# 11-18 신희원 예적금 데이터 중 최대금액 불러오기
@api_view(['GET'])
def recommend_upload(request):
    max_intr_rate2 = DepositOptions.objects.aggregate(intr_rate2=Max('intr_rate2'))['intr_rate2']
    options = DepositOptions.objects.filter(intr_rate2=max_intr_rate2)    
    # print(options[0])
    product=get_object_or_404(DepositProducts,fin_prdt_cd=options[0].fin_prdt_cd)

    # serializer1 = DepositOptionsSerializer(options)
    serializer2 = DepositProductsSerializer(product)
    return Response(serializer2.data)
    # return Response({'deposit_product':serializer2.data,'option':[serializer1.data]})

# 예적금 상품 ID로 불러오기
@api_view(['GET'])
def id_to_deposit(request):
    product_ids = []

    for key, value in request.GET.items():
        if 'product' in key:  # 'product' 파라미터를 찾고
            product_ids.append(int(value))  # product 값들을 배열에 추가 (int로 변환)

    products = DepositProducts.objects.filter(id__in=product_ids)
    serializer = DepositProductsSerializer(products, many=True)

    return Response(serializer.data)