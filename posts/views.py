from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from django.http import Http404
from .serializers import PostSerializer, PostDetailSerializer, PostValidateSerializer
from .serializers import CommentSerializer, CommentDetailSerializer, CommentValidateSerializer
from .models import Post, Comment
from .permissions import IsAuthorOrReadOnly



class ExceptionHandledAPIView(APIView):
    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return Response(
                {'error': str(exc)},
                status=status.HTTP_404_NOT_FOUND
            )
        return super().handle_exception(exc)
    

    
class PostListCreateAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination

    def post(self, request, *args, **kwargs):
        serializer = PostValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )
        author_id = serializer.validated_data.get('author_id')
        title = serializer.validated_data.get('title')
        body = serializer.validated_data.get('body')
        is_published = serializer.validated_data.get('is_published')

        post = Post.objects.create(
            author_id=author_id,
            title=title,
            body=body,
            is_published=is_published,
        )
        post.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=PostDetailSerializer(post).data
        )
    


class PostDetailAPIView(ExceptionHandledAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = 'id'

    def get_object(self):
        post_id = self.kwargs.get('id')
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise Http404(f'Post with id={post_id} does not exist!')
        
        self.check_object_permissions(self.request, post)
        return post

    
    def put(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = PostValidateSerializer(data=request.data, post=post)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        # Обновляем поля
        post.title = serializer.validated_data.get('title')
        post.body = serializer.validated_data.get('body')
        post.is_published = serializer.validated_data.get('is_published')
        post.save()

        return Response(status=status.HTTP_200_OK, data=PostDetailSerializer(post).data)
    





class CommentListCreateAPIView(ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        post_id = self.kwargs.get('id')
        return Comment.objects.filter(post_id=post_id)
    
    def post(self, request, *args, **kwargs):
        serializer = CommentValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )
        post_id = self.kwargs.get('id')
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise Http404(f'Post with id={post_id} does not exist!')

        comment = Comment.objects.create(
            post=post,
            author=request.user,
            body=serializer.validated_data.get('body'),
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data=CommentDetailSerializer(comment).data
        )
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []