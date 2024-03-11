from rest_framework import serializers
from users.models import Payment, User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # username = None
    # password = serializers.CharField(max_length=50)
    #
    # def create(self, validated_data):
    #     user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'],)
    #     return user

    class Meta:
        model = User
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token
