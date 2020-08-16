from rest_framework import serializers
from django.contrib.auth.models import Group


# ModelSerializer和Serializer
# 1、ModelSerializer可以根据model所指定模型类自动序列化器字段
# 2、ModelSerializer实现了create和update方法
# 3、如果模型类字段指定了,unique= 唯一值选项，ModelSerializer或自动生成唯一值判断方法
class GroupSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"  # 指定生成哪些字段
