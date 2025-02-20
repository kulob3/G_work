from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class BannedUserBackend(ModelBackend):
    """Класс для проверки пользователя на бан"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
            if user.banned:
                return None
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None