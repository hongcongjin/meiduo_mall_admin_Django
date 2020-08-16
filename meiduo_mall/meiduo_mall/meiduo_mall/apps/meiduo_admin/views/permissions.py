from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Permission, ContentType
from rest_framework.permissions import IsAdminUser

from meiduo_admin.serialziers.permissions import PerssionsSerialzier, ContentTypeSerialzier
from meiduo_admin.utils import PageNum


class PermissionsView(ModelViewSet):
    serializer_class = PerssionsSerialzier
    queryset = Permission.objects.all()
    pagination_class = PageNum
    permission_classes = []

    # 父类中没有权限类型表的操作，需要自己封装方法
    def content_type(self, request):
        """
            获取权限类型
        :param request:
        :return:
        """
        # 1、获取权限类型的所有数据
        data = ContentType.objects.all()

        # 2、序列化返回权限类型  self.get_serializer() 获取serializer_class属性所指定的序列器对象
        ser = ContentTypeSerialzier(data, many=True)  # 初始化生成序列化器对象

        return Response(ser.data)
