from django.urls import path
from . import views

urlpatterns = [
    path('friend-request/send/', views.SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/respond/<int:id>/', views.RespondToFriendRequestView.as_view(), name='respond-friend-request'),
    path('friend-request/pending/', views.ListPendingRequestsView.as_view(), name='list-pending'),
    path('friends/', views.ListFriendsView.as_view(), name='friends'),

]
