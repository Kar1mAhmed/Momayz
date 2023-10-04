from rest_framework import serializers
from .models import User

from dj_rest_auth.serializers import UserDetailsSerializer, PasswordResetSerializer



class UserRegisterSerializer(UserDetailsSerializer):

    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        exclude = ['is_superuser', 'is_staff', 'last_login', 'date_joined', 'is_active']
        extra_kwargs = {
            'password': {
                'write_only':True
            }
        }
    
    def save(self, request):  # Change the method signature here
        user = User(
            phone=self.validated_data['phone'],
            name=self.validated_data['name'],
            gender = self.validated_data['gender'],
            notification_token = self.validated_data['notification_token'], 
            govern = self.validated_data['govern']           
        )
        optional_fields = ['with_facebook', 'with_google', 'email']
    
        for field in optional_fields:
            if field in self.validated_data:
                setattr(user, field, self.validated_data[field])

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user
        

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        model = User
        exclude = ['is_superuser', 'is_staff', 'last_login', 'date_joined', 'is_active']