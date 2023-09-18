from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed

from .models import Article
from user.models import Follow, User
from notification.models import Notification


@receiver(post_save, sender=Article)

def notifacation_to_followers(instance, created, *args, **kwargs):
    if created:
        followers = instance.user.followers.all()

        for data in followers:
             follower = data.follower
             
             if not data.muted:
                 Notification.objects.create(
                    content_object=instance,
                    user=follower,
                    text=f'{instance.user.username} has added a new article ',
                    notification_type="Article"  # Utilisez "notification_type" ici
                )

                 

@receiver(post_save, sender=Follow)
def notifacation_to_users(instance, created, *args, **kwargs):
    if created:
        followed = instance.followed

        if not instance.muted:
            Notification.objects.create(
                content_object=instance,
                user=followed,
                text=f'{instance.follower.username} started following ',
                notification_type="Follow"  # Utilisez "notification_type" ici
            )


@receiver(m2m_changed, sender=Article.likes.through)
def send_notifacation_likes(instance, pk_set, action, *args, **kwargs):
    pk = list(pk_set)[0]
    user = User.objects.get(pk=pk)
 
    if action == "post_add":
        Notification.objects.create(
            content_object=instance,
            user=instance.user,
            text=f'{user.username} liked your lesson',
            notification_type="Like"  # Utilisez "notification_type" ici
        )
                



                 
