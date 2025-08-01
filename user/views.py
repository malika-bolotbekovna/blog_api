from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserAuthSerializer, UserCreateSerializer



class AuthAPIView(APIView):
    def post(slf, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)  # username='admin1', password='123'
        if user:
            print(user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={'error': 'user credentials are wrong!'}
        )





@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = User.objects.create_user(
        username=username, 
        password=password,
        is_active=True
    )
    return Response(
        data={'user_id': user.id},
        status=status.HTTP_201_CREATED
    )
