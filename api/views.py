from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from account.models import Verification
from account.views import email_sender
from .serializers import UserSerializer, UserUpdateSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@api_view(['POST'])
def user_create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    status = 'error'
    token = ''
    if user is not None:
        if user.is_verified:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            status = 'ok'
        else:
            status = 'not verified'
    res = {
        'token': token,
        'status': status
    }
    return Response(res)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_update(request):
    user = request.user
    email = request.data.get('email') != ''
    serializer = UserUpdateSerializer(instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        if email:
            print(request.data.get('email'))
            Verification.objects.get_or_create(user=request.user)
            email_sender(user.id)
            user.is_verified = False
            user.save()
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_password(request):
    email = request.user.email
    password = request.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
        password1 = request.data.get('new_password1')
        password2 = request.data.get('new_password2')
        if password1 == password2:
            user.set_password(password1)
            user.save()
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'passwords don\'t match'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'status': 'wrong password'}, status=status.HTTP_400_BAD_REQUEST)
