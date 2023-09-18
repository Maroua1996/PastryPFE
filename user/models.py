
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth.models import AbstractUser


from .managers import CustomUserManager

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(
     max_length=254,
        unique=True,
        error_messages={
            'unique': "A user with that email already exists.",
        },
    )
    image = models.ImageField(upload_to='image', 
    blank=True, 
    null=True)

    followers = models.ManyToManyField("Follow", blank=True)
    

    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    def __str__(self):
     return self.username

    def get_profile_image(self):
      url = ""
      try:
         url = self.image.url
      except:
        url = ""
      return url
      


class Follow(models.Model):
    followed = models.ForeignKey(
        User,
        related_name='user_followers',
        on_delete=models.CASCADE
    )
    follower = models.ForeignKey(
        User,
        related_name='user_follows',
        on_delete=models.CASCADE
    )
    muted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.follower.username} started following {self.followed.username}"

