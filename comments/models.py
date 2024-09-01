from django.db import models
from django.conf import settings  
from ads.models import Ad  

class Comment(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ad', 'user')

    def __str__(self):
        return f'Comment by {self.user} on {self.ad}'
