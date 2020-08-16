from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.permissions import IsAdminUser
from goods.models import SKU, GoodsCategory, SPU
from meiduo_admin.serialziers.skus import SKUSerialzier, GoodsCategorySerializer, SPUSpecificationSerializer
from meiduo_admin.utils import PageNum


class SKUVIew(ModelViewSet):
    # 指定序列化器
    serializer_class = SKUSerialzier
    # 指定查询集
    queryset = SKU.objects.all()
    # 指定分页器
    pagination_class = PageNum
    # 指定权限
    permission_classes = []

    # 重写获取查询集数据的方法
    def get_queryset(self):
        if self.request.query_params.get('keyword') == '':
            return SKU.objects.all()

        elif self.request.query_params.get('keyword') is None:
            return SKU.objects.all()

        else:
            return SKU.objects.filter(name__contains=self.request.query_params.get('keyword'))

    @action(methods=['get'], detail=False)
    def categories(self, request):
        """
            获取商品三级分类
        :param request:
        :return:
        """
        data = GoodsCategory.objects.filter(subs__id=None)
        ser = GoodsCategorySerializer(data, many=True)
        return Response(ser.data)

    def specs(self, request, pk):
        """
            获取spu商品规格信息
        :param request:
        :param pk:  spu表id值
        :return:
        """

        # 1、查询spu对象
        spu = SPU.objects.get(id=pk)
        # 2、关联查询spu所关联的规格表
        data = spu.specs.all()
        # 3、序列化返回规格信息
        ser = SPUSpecificationSerializer(data, many=True)
        return Response(ser.data)


        # def create(self, request, *args, **kwargs):
        #     # 1\
        #     #
        #     # 3\数据库保存
