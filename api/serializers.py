from rest_framework import serializers

from account.models import User
from lafyuu_ecommerce import settings
from shop.models import Product, ProductImage, ProductColor, ProductSize


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
        fields = ['password', ]


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'title']

    def get_image(self, obj):
        return settings.BASE_URL + str(obj.image.url)


class ProductColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['id', 'name', 'color']


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ['id', 'size']


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()
    benefit = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_images(self, obj):
        qs = obj.images
        print(qs)
        return ProductImageSerializer(qs, many=True).data

    def get_colors(self, obj):
        qs = obj.colors
        return ProductColorsSerializer(qs, many=True).data

    def get_sizes(self, obj):
        qs = obj.sizes
        return ProductSizeSerializer(qs, many=True).data

    def get_benefit(self, obj):
        return obj.get_benefit()
