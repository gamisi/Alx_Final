from django.shortcuts import render
from rest_framework import generics, viewsets
from .serializers import CustomUserSerializer, UserLoginSerializer, VehicleSerializer, MakeSerializer, ModelSerializer
from accounts.models import CustomUser
from garage.models import Vehicle, Make, Model
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework.reverse import reverse

class APIRoot(APIView):
    #permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.is_authenticated:
            # Redirect to the root URL
            return redirect(reverse('api:api-root'))  # Or redirect to a specific named URL using reverse()
        else:
            return Response({"message": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)      
    
# Create your views here.
class UserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

class MakeViewSet(viewsets.ModelViewSet):
    queryset = Make.objects.all()
    serializer_class = MakeSerializer
    permission_classes = [IsAuthenticated]

class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticated]

"""
    class VehicleListAPIView(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
"""
