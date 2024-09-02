from django.urls import path
from .views import GetUsers,SendFriendRequestView, AcceptRejectFriendRequestView, ListFriendsView, ListPendingFriendRequestsView

urlpatterns = [
    path('', GetUsers.as_view(), name='get-users'),
    path('request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('request/respond/', AcceptRejectFriendRequestView.as_view(), name='respond-friend-request'),
    path('friends/', ListFriendsView.as_view(), name='list-friends'),
    path('request/pending/', ListPendingFriendRequestsView.as_view(), name='pending-friend-requests'),
]
