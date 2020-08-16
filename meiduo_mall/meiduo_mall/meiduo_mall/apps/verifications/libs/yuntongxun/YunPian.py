import requests
import json

# def send_single_sms(apikey, code, mobile):
#     #发送单条短信
#     url = "https://sms.yunpian.com/v2/sms/single_send.json"
#     text = "【洪明焱test】您的验证码是{}.如非本人操作，请忽略此短信".format(code)
#
#     res = requests.post(url, data={
#         "apikey": apikey,
#         "mobile": mobile,
#         "text": text
#     })
#     return res

class CCP(object):
    def __new__(cls, *args, **kwargs):
        """
        定义单例的初始化方法
        :return: 单例
        """
        #判断单例是否存在，_instance属性中存储的就是单例
        if not hasattr(cls,'_instance'):
            cls._instance=super(CCP,cls).__new__(cls, *args, **kwargs)

            # 初始化REST SDK
        return cls._instance

    def send_single_sms(self,apikey, code, mobile):
        # 发送单条短信
        url = "https://sms.yunpian.com/v2/sms/single_send.json"
        text = "【洪明焱test】您的验证码是{}.如非本人操作，请忽略此短信".format(code)

        res = requests.post(url, data={
            "apikey": apikey,
            "mobile": mobile,
            "text": text
        })
        return res


if __name__ == '__main__':
    #单例类发送短信验证码
    CCP().send_single_sms("73be1ab7c254c563fce13bfff376b22f", "123456","13697986850")