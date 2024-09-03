from django.db import models
from account.models import User
# Create your models here.

class FriendRequest(models.Model):
    sender   = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self) -> str:
        return f"ReqID: {self.id} {self.sender} to {self.receiver} ({'Accepted' if self.is_accepted else 'Pending'})"
    
    
