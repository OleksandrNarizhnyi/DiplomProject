from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)  # Ищем пользователя по email
            if user.check_password(password):  # Проверяем пароль
                return user
        except UserModel.DoesNotExist:
            return None