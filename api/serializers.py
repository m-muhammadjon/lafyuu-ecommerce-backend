from rest_framework import serializers

from account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False, max_length=30)
    last_name = serializers.CharField(required=False, max_length=30)
    email = serializers.EmailField(required=False, max_length=30)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'gender', 'birthday', 'phone_number', ]

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password',]

