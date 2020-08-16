from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAdminUser

from meiduo_admin.serialziers.orders import OrederSerialzier
from meiduo_admin.utils import PageNum
from orders.models import OrderInfo


class OrderView(ReadOnlyModelViewSet):
    queryset = OrderInfo.objects.all()
    serializer_class = OrederSerialzier
    pagination_class = PageNum
    permission_classes = []

    # def get_object(self):
    #     queryset=self.get_queryset()
    #
    #     obj=self.get_func(queryset,{'pk':1})
    #
    #     return obj

    # 重写获取查询集数据的方法
    def get_queryset(self):
        if self.request.query_params.get('keyword') == '':
            return OrderInfo.objects.all()

        elif self.request.query_params.get('keyword') is None:
            return OrderInfo.objects.all()

        else:
            return OrderInfo.objects.filter(order_id__contains=self.request.query_params.get('keyword'))

    @action(methods=['put'],detail=True)            #需要正则匹配
    def status(self, request, pk):
        """
            修改订单状态
        :param request:
        :PK  订单编号
        :return:
        """

        # 1、查询要修改的订单对象
        try:
            order = OrderInfo.objects.get(order_id=pk)
        except:
            return Response({'error': '订单编号错误'})

        # 2、修改订单状态
        # 获取订单状态
        status = request.data.get('status')
        if status is None:
            return Response({'error': '缺少状态值'})
        order.status = status
        order.save()
        # 3、返回修改信息
        return Response(
            {
                'order_id': pk,
                'status': status
            }
        )
