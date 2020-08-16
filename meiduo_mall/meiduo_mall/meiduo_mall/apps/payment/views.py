from django.shortcuts import render
from django.views import View
from alipay import AliPay
# from django.conf import settings
from meiduo_mall.settings import dev
import os
from django import http

from meiduo_mall.utils.views import LoginRequiredJSONMixin
from orders.models import OrderInfo
from meiduo_mall.utils.response_code import RETCODE
from payment.models import Payment
# Create your views here.

#使用ubuntu生成的app_private_key.pem
# 买家账号khrvkp5814@sandbox.com
# 登录密码111111
# 支付密码111111
# 用户名称沙箱环境
# 证件类型身份证(IDENTITY_CARD)
# 证件号码759460193401229514

#商家账号kpnavn8755@sandbox.com
# 商户UID2088621955035800
# 登录密码111111

app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAxfxpNzWctWRPRVfp/X5l26Z2jVvJxngJh9H7MH4bhVTwNPEm
iMy7Ic5bZoZOaStfn+QcT18606W7Teqttf1RZZAvLPoz7gt/bYBTlhyHo36YjvJW
lklIvYmCPf6sweNOvPvoFpZnSERj8IWKqboaSm9P++/QODQ1tg/cdonhHTP8O4pC
eWaZ/HgsaDV12ogK1vu22pI5wQhw8Edb9QDtUK3qscZ7zQN1u+21r9Kl7924B4/g
xWcjoxXjuKVKRYHezeSlgsyW41rELVYFxEr0FUXerKsZ14keUT1JKkH/cqMmmoBp
3t9v2P0t/9+gvY0Tov1XOI/zKIk0Pnm3aSOwqQIDAQABAoIBAQCWOjCb89I00ShV
NaAW+RHQ2T6bhEpWjj6tEGfJI+c+BHU/trvGkZJs1GgGI2Lb6k1kxXG1yEyay+aT
+L5WmSBqMD2boz5EIfVO4VCLVpqVNDoOPVP2NSU8rFpnMBdmB1R3ka1JdlZoP3yV
xL6yisPoNw453H3iJ7uZqe9fAsANp04wOMrlMPTJWj2bHukYrCiBh4ffl+hHLSlG
J5+G7fOCpvmTbKPDLWVE7sCMQan+mdQAjDpB3dIY2yCYW53wXhNlfl8be9494WGY
A8rMBZw08EZEQK2K7nI9tUr4AsePP3FkNnnqEm/BLaqo0AkhcA8KijiXiz/6FUNb
6Q3VJAABAoGBAO9i4/JLgnRGUR+7y1coE467HzJkj3EFfxosrbx0BrQJc02KJnkM
8hR2U8RFBUQsPuA+w79r7YvadOVFnxaV2cfE8Bb90uY5nkT7rjgtBuwo4PxWsp+D
uhIPdoficKQI2FsB/LtykxpZSzy5V9Br+4td5nK3U5dPCIeTHvitz1ApAoGBANO5
+QkwOAdt67VrCD6zASnVxBaLl6pC1thP3knuSvkcQt6/pP+J8jOLrQYzHC0MFa/I
TU9nMFjnCXhrIup7SoAeR49f74I9V4QriFLyHZrlaTEjho202+lvXpjaCGGUlmfp
W/1ULuDDvpD0MJNw50ZnOXiX8xhHxDq/jZkuY2yBAoGBAKw5a2GwbaSVyluYUkzc
KmXvvhwVORXJLI56Qmxo1UHF4syQbel9JNUP5Gg6d/V6F6phvZcEYRzTCHLCyhgH
q20MBOelqYu1PGbI46jKzEYvit5AybX1oXLI6TAN+5goPPAM1/VMEwVL5NNFTSZH
6et0nQ0/U8ZyN+LCN/AVrCcxAoGBAJwDmgKvSVoQIXQZXoX1GZJeNpP2YNfRUMcs
czw/H3fY312MEmVKnPJmpiS/XK/FC+XvzygHfZTFCjF1oNDv8MHfjhOUOcTatrZp
7ZZRWoddLNpMt0WMU8/7hNVVNH/TIdGIH4TYl4KAOthNV84NkB5MygiWz0bA+1Pe
+tQ5XoIBAoGAZAhP6eXov6VO+t1oRgYHAJ653PsqCWrGhLh8POIGwCMAOQDYKOwc
+TVnEOKtv051gYmVhztx2ZywqSAAJ4YryGc4j8ltrwT648uXsNBWrdZnpBpUVxpq
WjmKcqf+H9uom1Auhy1uBixjHdl6uCll3g3C1JSJFNFgT908pHgNidY=
-----END RSA PRIVATE KEY-----"""
alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxfxpNzWctWRPRVfp/X5l
26Z2jVvJxngJh9H7MH4bhVTwNPEmiMy7Ic5bZoZOaStfn+QcT18606W7Teqttf1R
ZZAvLPoz7gt/bYBTlhyHo36YjvJWlklIvYmCPf6sweNOvPvoFpZnSERj8IWKqboa
Sm9P++/QODQ1tg/cdonhHTP8O4pCeWaZ/HgsaDV12ogK1vu22pI5wQhw8Edb9QDt
UK3qscZ7zQN1u+21r9Kl7924B4/gxWcjoxXjuKVKRYHezeSlgsyW41rELVYFxEr0
FUXerKsZ14keUT1JKkH/cqMmmoBp3t9v2P0t/9+gvY0Tov1XOI/zKIk0Pnm3aSOw
qQIDAQAB
-----END PUBLIC KEY-----"""

class PaymentStatusView(LoginRequiredJSONMixin, View):
    """保存支付的订单状态"""

    def get(self, request):
        # 获取到所有的查询字符串参数
        query_dict = request.GET

        # 将查询字符串参数的类型转成标准的字典类型
        data = query_dict.dict()

        # 从查询字符串参数中提取并移除 sign，不能参与签名验证
        signature = data.pop('sign')

        # 创建SDK对象
        alipay = AliPay(  # 传入公共参数（对接任何接口都要传递的）
            appid=dev.ALIPAY_APPID,  # 应用ID
            app_notify_url=None,  # 默认回调url，如果采用同步通知就不传
            # 应用的私钥和支付宝公钥的路径
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # 加密标准
            debug=dev.ALIPAY_DEBUG  # 指定是否是开发环境
        )

        # 使用SDK对象，调用验通知证接口函数，得到验证结果
        success = alipay.verify(data, signature)

        # 如果验证通过，需要将支付宝的支付状态进行处理（将美多商城的订单ID和支付宝的订单ID绑定，修改订单状态）
        if success:
            # 美多商城维护的订单ID
            order_id = data.get('out_trade_no')
            # 支付宝维护的订单ID
            trade_id = data.get('trade_no')
            Payment.objects.create(
                # order = order
                order_id = order_id,
                trade_id = trade_id
            )
            # 修改订单状态由"待支付"修改为"待评价"
            OrderInfo.objects.filter(order_id=order_id, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']).update(
                status=OrderInfo.ORDER_STATUS_ENUM["UNCOMMENT"])

            # 响应结果
            context = {
                'trade_id': trade_id
            }
            return render(request, 'pay_success.html', context)
        else:
            return http.HttpResponseForbidden('非法请求')


class PaymentView(LoginRequiredJSONMixin, View):
    """对接支付宝的支付接口"""

    def get(self, request, order_id):
        """
        :param order_id: 当前要支付的订单ID
        :return: JSON
        """
        user = request.user
        # 校验order_id
        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'])
        except OrderInfo.DoesNotExist:
            return http.HttpResponseForbidden('订单信息错误')

        # 创建对接支付宝接口的SDK对象
        alipay = AliPay(  # 传入公共参数（对接任何接口都要传递的）
            appid=dev.ALIPAY_APPID,  # 应用ID
            app_notify_url=None,  # 默认回调url，如果采用同步通知就不传
            # 应用的私钥和支付宝公钥的路径
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # 加密标准
            debug=False # 指定是否是开发环境
        )

        # SDK对象对接支付宝支付的接口，得到登录页的地址
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id, # 订单编号
            total_amount=str(order.total_amount), # 订单支付金额
            subject="美多商城%s" % order_id, # 订单标题
            return_url=dev.ALIPAY_RETURN_URL # 同步通知的回调地址，如果不是同步通知，就不传
        )

        # 拼接完整的支付宝登录页地址
        # 电脑网站支付(正式环境)，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        # 电脑网站支付(开发环境)，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
        alipay_url = dev.ALIPAY_URL + '?' + order_string
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'alipay_url': alipay_url})
