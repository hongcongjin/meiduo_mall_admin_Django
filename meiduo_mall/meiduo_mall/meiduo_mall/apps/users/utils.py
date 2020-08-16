# 自定义用户认证的后端:实现多账号登录
from django.contrib.auth.backends import ModelBackend
import re
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from users.models import User
from itsdangerous import BadData
from meiduo_mall.settings import dev
from users.models import User
from . import constants

def check_verify_email_token(token):
    """
    反序列化token,获取到user
    :param token: 序列化后的用户信息
    :return: user
    """
    s = Serializer(dev.SECRET_KEY, constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    try:
        data = s.loads(token)
    except BadData:
        return None
    else:
        # 从data中取出user_id和email
        user_id = data.get('user_id')
        email = data.get('email')
        try:
            user = User.objects.get(id=user_id, email=email)
        except User.DoesNotExist:
            return None
        else:
            return user


def generate_verify_email_url(user):
    """
    生成邮箱激活链接
    :param user: 当前登录用户
    :return: http://www.meiduo.site:8000/emails/verification/?token=eyJhbGciOiJIUzUxMiIsImlhdCI6MTU1ODA2MDE0MSwiZXhwIjoxNTU4MTQ2NTQxfQ.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6InpoYW5namllc2hhcnBAMTYzLmNvbSJ9.y1jaafj2Mce-LDJuNjkTkVbichoq5QkfquIAhmS_Vkj6m-FLOwBxmLTKkGG0Up4eGGfkhKuI11Lti0n3G9XI3Q
    """
    s = Serializer(dev.SECRET_KEY, constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    data = {'user_id': user.id, 'email': user.email}
    token = s.dumps(data)
    return dev.EMAIL_VERIFY_URL + '?token=' + token.decode()

def get_user_by_account(account):
    """
    通过账号获取用户
    :param account: 用户名或者手机号
    :return: user
    """
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            # account == 手机号
            user = User.objects.get(mobile=account)
        else:
            # account == 用户名
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user

class UsernameMobileBackend(ModelBackend):
    """自定义用户认证后端"""

    # def authenticate(self, request, username=None, password=None, **kwargs):
    #     """
    #     重写用户认证的方法
    #     :param username: 用户名或手机号
    #     :param password: 密码明文
    #     :param kwargs: 额外参数
    #     :return: user
    #     """
    #是超级管理员用户request为None
    def authenticate(self, request, username=None, password=None, **kwargs):
        if request is None:
            # 后台登录
            try:
                # is_superuser判断用户是否是超级管理员用户
                user = User.objects.get(username=username, is_superuser=True)
            except:
                user = None

            if user is not None and user.check_password(password):
                return user


        else:
            try:
                # if re.match(r'^1[3-9]\d{9}$', username):
                #     user = User.objects.get(mobile=username)
                # else:
                #     user = User.objects.get(username=username)
                user = User.objects.get(username=username)
            except:
                # 如果未查到数据，则返回None，用于后续判断
                try:
                    user = User.objects.get(mobile=username)
                except:
                    return None
                    # return None

            # 判断密码
            if user.check_password(password):
                return user
            else:
                return None
        # # 查询用户
        # user = get_user_by_account(username)
        #
        # # 如果可以查询到用户，好需要校验密码是否正确
        # if user and user.check_password(password):
        #     # 返回user
        #     return user
        # else:
        #     return None