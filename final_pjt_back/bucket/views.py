from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Bucket
from finlife.models import DepositProducts
from rest_framework import status
from .serializers import BucketSerializer
from django.shortcuts import get_list_or_404, get_object_or_404


# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def bucket(request):
    user = request.user
    if request.method=="GET":
        buckets = get_list_or_404(Bucket, user=user)
        serializer = BucketSerializer(buckets, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        product_id = request.data.get('product_id')
        product = get_object_or_404(DepositProducts, id=product_id)
        # 장바구니에 있으면

        existing_bucket = Bucket.objects.filter(user=user, product=product).first()
        # existing_bucket= Bucket.objects.filter(product=product, user=user).exists():
        if existing_bucket:
            existing_bucket.delete()
            return Response({"message": False}, status=status.HTTP_200_OK)
        else:
            # 장바구니에 상품이 없으면 추가
            Bucket.objects.create(user=user, product=product)
            return Response({"message": True}, status=status.HTTP_201_CREATED)
        
    if request.method == 'DELETE':
        product_id = request.data.get('product_id')
        product = get_object_or_404(DepositProducts, id=product_id)

        existing_bucket = Bucket.objects.filter(user=user, product=product).first()
        # existing_bucket= Bucket.objects.filter(product=product, user=user).exists():
        if existing_bucket:
            existing_bucket.delete()
            return Response({"message": False}, status=status.HTTP_200_OK)
        else:
            return Response({"message" : "해당 상품은 없어요."})

@api_view(['GET'])
def check_if_product_in_bucket(request):
    product_id = request.query_params.get('product_id')
    if not product_id:
        return Response({"error": "상품 ID가 필요합니다."}, status=400)

    product = get_object_or_404(DepositProducts, id=product_id)
    # 장바구니에 해당 상품이 있는지 확인
    existing_bucket = Bucket.objects.filter(user=request.user, product=product).first()

    
    if existing_bucket:
        # 장바구니에 해당 상품이 존재하면
        return Response({"isAdded": True})
    else:
        # 장바구니에 해당 상품이 없으면
        return Response({"isAdded": False})