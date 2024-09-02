from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer
from accunox.renderers import CustomJSONRenderer
from .models import CustomUser


def get_tokens(user):
    refresh=RefreshToken.for_user(user)
    # print(refresh)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token)
    }


class UserRegistration(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Allow any user to access registration

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens(user)
            return Response({
                'message': 'ok',
                'token': token,
                'user': {
                    'name': user.name,
                    'email': user.email,
                    'id': user.id
                }
            }, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            return Response({"message":"error","error":errors},status=400)

class UserLogin(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    def post(self,request,format=None):
        email=request.data.get('email')
        password=request.data.get('password')
        user=authenticate(email=email,password=password)
        if(user!=None):
            token=get_tokens(user)
            return Response({
                'msg':'Login Successfull',
                'token':token,
                'user': {
                    'name': user.name,
                    'email': user.email,
                    'id': user.id
            }
            }
            ,status=200)
        else:
            return Response({"message":"error","error":"Credentials not valid"},status=400)

        
