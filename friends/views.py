from django.db.models import Q
from django.core.cache import cache
from rest_framework.exceptions import Throttled

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from .models import FriendRequest
from .serializers import FriendRequestSerializer, FriendRequestActionSerializer, ListFriendsSerializer
from account.models import User

# Create your views here.

class SendFriendRequestView(generics.CreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        receiver_id = self.request.data.get('receiver_id')
        try:
            receiver = User.objects.get(id=receiver_id)

            # Get the cache key for the current user
            cache_key = f"friend_request_count_{self.request.user.id}"
            friend_request_count = cache.get(cache_key, 0)

            # Check if the user has already sent 3 friend requests within the last minute
            if friend_request_count >= 3:
                raise Throttled()


            if FriendRequest.objects.filter(sender=self.request.user, receiver=receiver).exists():
                raise serializers.ValidationError({"message": "Friend request already sent."})
            
            if FriendRequest.objects.filter(sender=receiver, receiver=self.request.user).exists():
                raise serializers.ValidationError({"message": "This user has already sent you a friend request."})
            
            if receiver == self.request.user:
                raise serializers.ValidationError({"message": "You cannot send request to self."})
            
            serializer.save(sender=self.request.user, receiver=receiver)

            # Update the cache with the new friend request count
            cache.set(cache_key, friend_request_count + 1, timeout=60)  # Expires in 60 seconds

        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "Receiver not found."})
        

class RespondToFriendRequestView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FriendRequest.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestActionSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        friend_request = self.get_object()

        if friend_request.receiver != request.user:
            return Response({"message": "You cannot respond to this request"}, status=status.HTTP_403_FORBIDDEN)
        
        action_serializer = self.get_serializer(data=request.data)
        action_serializer.is_valid(raise_exception=True)
        action = action_serializer.validated_data['action']

        if action == 'accept':
            friend_request.is_accepted = True
            friend_request.save()
            return Response({"detail": "Friend request accepted."}, status=status.HTTP_200_OK)
        elif action == 'reject':
            friend_request.delete()
            return Response({"detail": "Friend request rejected."}, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        friend_request = self.get_object()

        if friend_request.receiver != request.user:
            return Response({"detail": "You cannot delete this friend request."}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)
    

class ListPendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return FriendRequest.objects.filter(receiver=user, is_accepted=False)


class ListFriendsView(generics.ListAPIView):
    serializer_class = ListFriendsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        accepted_requests = FriendRequest.objects.filter(
            Q(sender=user, is_accepted=True) | Q(receiver=user, is_accepted=True)
        )
        friend_ids = set()
        for request in accepted_requests:
            if request.sender == user:
                friend_ids.add(request.receiver.id)
            else:
                friend_ids.add(request.sender.id)
        return User.objects.filter(id__in=friend_ids)
    