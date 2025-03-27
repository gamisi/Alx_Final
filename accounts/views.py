from django.shortcuts import render
from rest_framework import generics, viewsets
from .serializers import CustomUserSerializer, UserLoginSerializer
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token

# Create your views here.
class UserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class UserLoginView(APIView):
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'here is your token': {token.key}}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
def register(request):
    return render(request, 'accounts/register.html')

def home (request):
    return render(request, 'accounts/login.html')
