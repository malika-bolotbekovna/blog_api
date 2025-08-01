from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = 'id author title'.split()


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post 
        fields = '__all__'


class PostValidateSerializer(serializers.Serializer):
    author_id = serializers.IntegerField()
    title = serializers.CharField(required=True, min_length=1, max_length=50)
    body = serializers.CharField(required=False)
    is_published = serializers.BooleanField(default=True)
    
    def __init__(self, *args, **kwargs):
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)

    def validate_author_id(self, author_id):
        try:
            user=User.objects.get(id=author_id)
        except User.DoesNotExist:
            raise ValidationError('User does not exist!')
        
        if not user.is_active:
            raise serializers.ValidationError("User is not active!")
        
        if self.post and self.post.author.id != author_id:
            raise serializers.ValidationError("You cannot change the author of the post!")

        return author_id




class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = 'author body post is_approved'.split()

 
class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment 
        fields = '__all__'


class CommentValidateSerializer(serializers.Serializer):
    body = serializers.CharField(required=True, allow_blank=False)
    