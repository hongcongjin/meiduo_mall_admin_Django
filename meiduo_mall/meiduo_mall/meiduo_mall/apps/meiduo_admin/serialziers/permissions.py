from rest_framework import serializers
from django.contrib.auth.models import Permission, ContentType


class PerssionsSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'



class ContentTypeSerialzier(serializers.ModelSerializer):
    """
        权限类型序列化器
    """
    name=serializers.CharField(read_only=True)
    class Meta:
        model = ContentType  # 指定根据那个模型类生成序列化字段
        fields = '__all__'  # 指定生成哪些字段
