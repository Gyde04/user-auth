# Importing necessary decorators from Django Rest Framework
from rest_framework.decorators import api_view, authentication_classes, permission_classes

# Importing Response class for handling API responses
from rest_framework.response import Response

# Importing status codes to denote HTTP status in responses
from rest_framework import status

# Importing authentication classes for API endpoints
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

# Importing permission classes to control access to API endpoints
from rest_framework.permissions import IsAuthenticated

# Importing the User model from Django's built-in authentication system
from django.contrib.auth.models import User

# Importing a helper function to get an object or 404 error if not found
from django.shortcuts import get_object_or_404

# Importing Token model to manage authentication tokens
from rest_framework.authtoken.models import Token


from .serializers import UserSerializer

@api_view(['POST'])
def login(request):
    """
    Log in a user and return a token.
    """
    try:
        user = get_object_or_404(User, username=request.data.get('username'))
        if not user.check_password(request.data.get('password')):
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)
        return Response({"token": token.key, "user": serializer.data})
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def signup(request):
    """
    Sign up a new user.
    """
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(username=request.data.get('username'), password=request.data.get('password'))
            token = Token.objects.create(user=user)
            return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    """
    Test authentication token.
    """
    return Response("Authentication passed for {}".format(request.user.username))
