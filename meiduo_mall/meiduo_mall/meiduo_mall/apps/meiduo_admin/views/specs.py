from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from goods.models import SPUSpecification
from goods.models import SPU
from meiduo_admin.serialziers.specs import SpecsSerialzier, SPUSerializer
from meiduo_admin.utils import PageNum


class SpecsView(ModelViewSet):
    """
        商品规格的增删改查
    """
    # 指定查询集
    queryset = SPUSpecification.objects.all()
    # 指定序列化器
    serializer_class = SpecsSerialzier

    pagination_class = PageNum

    def simple(self, request):
        """
            获取SPU商品
        :param request:
        :return:
        """
        spus = SPU.objects.all()
        ser = SPUSerializer(spus, many=True)

        return Response(ser.data)


