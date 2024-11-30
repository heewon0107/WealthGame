from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Comment, DepositProducts
from .serializers import CommentSerializer
from rest_framework import status
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.authentication import TokenAuthentication

@api_view(['GET'])
def get_comments(request, product_id):
    product = DepositProducts.objects.get(id=product_id)
    comments = Comment.objects.filter(product=product)
    serializer = CommentSerializer(comments, many=True)
    return Response({"comments": serializer.data})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])

# @permission_classes([IsAuthenticated])  # 로그인한 사용자만 댓글 작성 가능
def post_comment(request):
    if request.method == 'POST':
        product_id = request.data.get('product_id')
        content = request.data.get('content')
        tier = request.data.get('tier', '알거지')
        product = DepositProducts.objects.get(id=product_id)
        # 댓글 작성
        comment = Comment.objects.create(
            user=request.user,
            product=product,
            content=content,
            tier=tier
        )

        serializer = CommentSerializer(comment)
        return Response({"comment": serializer.data}, status=status.HTTP_201_CREATED)

# 댓글 수정
@api_view(['PUT'])
# @permission_classes([IsAuthenticated])
def update_comment(request):
    try:
        product_id = request.data['params'].get('product_id')
        comment_id = request.data['params'].get('comment_id')  # 요청 본문에서 comment_id
        content = request.data['params'].get('content')
       
        comment = get_object_or_404(Comment, product_id=product_id, id=comment_id)
            
        comment.content = content
        comment.save()
        
        return Response({"message": "수정이 완료되었습니다.", "comment": {
            "id": comment.id,
            "content": comment.content,
            "nickname": comment.user.nickname,  # 사용자 닉네임도 포함
        }}, status=status.HTTP_200_OK)

    except Comment.DoesNotExist:
        return Response(
            {"error": "Comment not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
def delete_comment(request):
    try:
        product_id = request.query_params.get('product_id')
        comment_id = request.query_params.get('comment_id')
        
        comment = get_object_or_404(Comment, product_id=product_id, id=comment_id)
        # 댓글 작성자와 현재 로그인한 사용자가 같은지 확인
            
        comment.delete()
        return Response({
            "message": "Comment deleted successfully"
        }, status=status.HTTP_200_OK)
        
    except Comment.DoesNotExist:
        return Response(
            {"error": "Comment not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def check_authentication(request):
    if request.user.is_authenticated:
        return Response({'is_authenticated': True})
    else:
        return Response({'is_authenticated': False})