from rest_framework import serializers
from demo import models
from django.contrib.auth.models import User


# class DemoSerializer(serializers.Serializer):
#     # 每一个表都可以建一个serializer，类似Django的Form  专门用于json
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     active = serializers.BooleanField(required=False, default=True)
#
#     def create(self, validated_data):
#         """
#         创建并返回一个新的`Demo`实例, 传入验证过的数据.
#         """
#         return Demo.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         更新并返回一个已存在的实例，传入验证过的数据
#         :param instance:
#         :param validated_data:
#         :return: instance
#         """
#         instance.name = validated_data.get('name', instance.name)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance


class DemoSerializer(serializers.ModelSerializer):
    # ModelSerializer和Django中ModelForm功能相似
    # Serializer和Django中Form功能相似

    # def create(self, validated_data):
    #     return super(DemoSerializer, self).create(validated_data)

    class Meta:
        model = models.Demo
        fields = ('id', 'name', 'active')

class SaleOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SaleOrder
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserTokenSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = models.UserToken
        fields = ('token', 'address', 'user')
