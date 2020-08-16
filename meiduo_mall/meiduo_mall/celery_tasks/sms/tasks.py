# 定义任务
from celery_tasks.sms.yuntongxun.YunPian import CCP
from . import constants
from celery_tasks.main import celery_app


# 使用装饰器装饰异步任务，保证celery识别任务
@celery_app.task(name='send_single_sms')
def send_sms_code(mobile, sms_code):
    """
    发送短信验证码的异步任务
    :param mobile: 手机号
    :param sms_code: 短信验证码
    :return: 成功：0 、 失败：-1
    """
    send_ret = CCP().send_single_sms("73be1ab7c254c563fce13bfff376b22f",sms_code,mobile)
    return send_ret