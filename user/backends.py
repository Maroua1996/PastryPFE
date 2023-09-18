from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist

from user.models import User

class EmailAuthentificationBackend(ModelBackend):
    def authenticate(self, request, *args, username=None, password=None,  **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            else:
                return None
                
        except ObjectDoesNotExist:
            return None
            
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except ObjectDoesNotExist:
            return None
