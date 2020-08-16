from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import Group, Permission
from django.urls import reverse
from meiduo_admin.serialziers.group import GroupSerialzier
from meiduo_admin.serialziers.permissions import PerssionsSerialzier
from meiduo_admin.utils import PageNum


class GroupView(ModelViewSet):
    # 父类方法需要调用序列化器
    serializer_class = GroupSerialzier
    # 视图集属性
    queryset = Group.objects.all()
    # 分页属性
    pagination_class = PageNum
    # 权限属性
    permission_classes = []

    # @action(methods=['get'],detail=False)  # methods指定方法所对应的请求方式 detail指定在生成的路径中是否需要正则匹配
    def simple(self, request):
        """
            获取权限数据
        :param request:
        :return:
        """
        # 1、查询权限表
        data = Permission.objects.all()
        # 2、返回权限数据

        ser = PerssionsSerialzier(data, many=True)

        return Response(ser.data)
