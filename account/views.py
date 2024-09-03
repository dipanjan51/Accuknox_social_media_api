from django.contrib.auth import authenticate
from django.db.models import Q

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status

from .models import User
from .serializers import UserModelSerializer, UserLoginSerializer, SearchSerializer
# Create your views here.

class UserSignUpView(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()

    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     return user
    
    
class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user= serializer.validated_data['user']
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            })
        else:
            return Response({"non_field_errors": ["Invalid login credentials"]}, status=status.HTTP_400_BAD_REQUEST)
        

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "User logged out"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"message": "No token found for this user."}, status=status.HTTP_400_BAD_REQUEST)
        

class SearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SearchSerializer

    def get_queryset(self):
        search_keyword = self.request.query_params.get('search', '')

        if '@' in search_keyword:
            return User.objects.filter(email=search_keyword)
        
        else:
            return User.objects.filter(
                Q(first_name__icontains=search_keyword) |
                Q(last_name__icontains=search_keyword)
            )
