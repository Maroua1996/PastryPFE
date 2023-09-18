from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from user.models import User

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('Article', 'Article'),
        ('Like', 'Like'),
        ('Follow', 'Follow')
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_seen = models.BooleanField(default=False)
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES
    )
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
