from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from datetime import date, timedelta

from meiduo_admin.serialziers.statistical import UserGoodsCountSerializer
from users.models import User
from goods.models import GoodsVisitCount


class UserCountView(APIView):
    """
        用户总量统计
    """
    # 权限指定
    permission_classes = []

    def get(self, request):
        # 1、获取当天日期
        now_date = date.today()
        # 2、获取用户总量
        count = User.objects.all().count()
        # 3、返回结果
        return Response({
            'date': now_date,
            'count': count
        })


class UserDayCountView(APIView):
    """
        日增用户统计
    """
    # 权限指定
    permission_classes = []

    def get(self, request):
        # 1、获取当天日期
        now_date = date.today()
        # 2、获取当天注册用户总量
        count = User.objects.filter(date_joined__gte=now_date).count()
        # 3、返回结果
        return Response({
            'date': now_date,
            'count': count
        })


class UserDayActiveCountView(APIView):
    """
        日活用户统计
    """
    # 权限指定
    permission_classes = []

    def get(self, request):
        # 1、获取当天日期
        now_date = date.today()
        # 2、获取当天登录用户总量
        count = User.objects.filter(last_login__gte=now_date).count()
        # 3、返回结果
        return Response({
            'date': now_date,
            'count': count
        })


class UserDayOrdersCountView(APIView):
    """
        下单用户统计
    """
    # 权限指定
    permission_classes = []

    def get(self, request):
        # 1、获取当天日期
        now_date = date.today()
        # 2、获取当天下订单用户总量
        count = len(set(User.objects.filter(orders__create_time__gte=now_date)))

        # 3、返回结果
        return Response({
            'date': now_date,
            'count': count
        })


class UserMonthCountView(APIView):
    """
        月增用户统计
    """
    # 权限指定
    permission_classes = []

    def get(self, request):
        # 1、获取当天日期
        now_date = date.today()
        # 2、获取一个月之前的日期
        begin_date = now_date - timedelta(days=59)
        data_list = []
        for i in range(60):
            # 起始日期
            indxe_date = begin_date + timedelta(days=i)
            # 第二天的日期(起始日期的下一天日期)
            next_date = begin_date + timedelta(days=i + 1)
            count = User.objects.filter(date_joined__gte=indxe_date, date_joined__lt=next_date).count()
            data_list.append({
                'count': count,
                'date': indxe_date
            })
        return Response(data_list)


class UserGoodsCountView(APIView):
    """
        日分类商品访问量统计
    """
    # 权限指定
    permission_classes = []

    def get(self, request):
        # 1、获取当天日期
        now_date = date.today()
        # 2、获取当天分类访问数量
        goods = GoodsVisitCount.objects.filter(date__gte=now_date)

        ser = UserGoodsCountSerializer(goods, many=True)
        # 3、返回结果
        return Response(ser.data)
