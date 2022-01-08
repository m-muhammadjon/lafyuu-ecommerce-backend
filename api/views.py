from django.contrib.auth import authenticate
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from account.models import Verification
from account.views import email_sender
from shop.filters import ProductFilter
from shop.models import Product
from .serializers import UserSerializer, UserUpdateSerializer, ProductSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# User API

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
            Verification.objects.get_or_create(user=request.user)
            email_sender(user.id)
            user.is_verified = False
            user.save()
            return Response({'message': 'We Will Send verification to your New Email'}, status=status.HTTP_200_OK)
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


# Product API

'''
from django.db import connection, reset_queries
import time
import functools


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)
        print(connection.queries)
        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        return result

    return inner_func

@query_debugger
def book_list(re):
    queryset = Product.objects.all()
        # .prefetch_related("images") \
        # .prefetch_related("colors") \
        # .prefetch_related("sizes") \
        # .all()
    data = ProductSerializer(queryset, many=True,).data
    return JsonResponse({"data":data})
    # return books
'''


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('images') \
        .prefetch_related('sizes') \
        .prefetch_related('colors') \
        .all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter
