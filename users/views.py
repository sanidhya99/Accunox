from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from authentication.serializers import UserSerializer
from authentication.models import CustomUser
from .models import Request
from .serializers import RequestSerializer

class CustomPagination(PageNumberPagination):
    page_size = 10

class GetUsers(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        search_keyword = self.request.query_params.get('search', None)

        if search_keyword:
            # Check if the search keyword matches an exact email
            exact_match = queryset.filter(email=search_keyword).first()
            if exact_match:
                return CustomUser.objects.filter(id=exact_match.id)

            # Perform partial match on name
            queryset = queryset.filter(name__icontains=search_keyword)

        return queryset
    
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.paginate_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return self.get_paginated_response({'message':'ok', 'data': serializer.data,'status': 200})
        except Exception as e:
            return Response({'message':'Error occurred while fetching data', 'error': str(e), 'status': 400, 'status_text':'error'}, status=400)


class SendFriendRequestView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        sender = request.user
        subject_id = request.data.get('subject_id')
        
        if not subject_id:
            return Response({"message": "error","error":"Subject_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        subject = CustomUser.objects.get(id=subject_id)
        if sender == subject:
            return Response({"message": "error","error":"You cannot send a friend request to yourself"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if there's already a friend request or if they are already friends
        if Request.objects.filter(sender=sender, subject=subject).exists():
            return Response({"message": "error","error":"Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)
        if subject.friends.filter(id=sender.id).exists():
            return Response({"message": "error","error":"You are already friends"}, status=status.HTTP_400_BAD_REQUEST)

        # Check request limit within 1 minute
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        if Request.objects.filter(sender=sender, created_at__gte=one_minute_ago).count() >= 3:
            return Response({"message": "error","error":"You cannot send more than 3 friend requests within a minute"}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # Create friend request
        friend_request = Request(sender=sender, subject=subject)
        friend_request.save()

        return Response({"message": "ok","success":"Friend request sent successfully"}, status=status.HTTP_201_CREATED)

class AcceptRejectFriendRequestView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_id = request.data.get('request_id')
        action = request.data.get('action')

        try:
            friend_request = Request.objects.get(id=request_id, subject=request.user)
        except Request.DoesNotExist:
            return Response({"message": "error","error":"Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

        if action == 'accept':
            request.user.friends.add(friend_request.sender)
            friend_request.sender.friends.add(request.user)  # Add the reciprocal relationship
            friend_request.delete()
            return Response({"message": "ok","success":"Friend request accepted"}, status=status.HTTP_200_OK)
        elif action == 'reject':
            friend_request.delete()
            return Response({"message": "ok","success":"Friend request rejected"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "error","error":"Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

class ListFriendsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.request.user.friends.all()

class ListPendingFriendRequestsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer

    def get_queryset(self):
        return Request.objects.filter(subject=self.request.user, accept=False)