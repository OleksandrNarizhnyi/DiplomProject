from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyCustomJWTSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        data = super().get_token(user)

        data['role'] = user.role

        return data