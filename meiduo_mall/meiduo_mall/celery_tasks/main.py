# Celery的入口
from celery import Celery


# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'

# 创建Celery实例
celery_app = Celery('meiduo')

# 加载配置
celery_app.config_from_object('celery_tasks.config')

# 注册任务
celery_app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.email', 'celery_tasks.static_file'])

#启动celery异步命令
#celery -A celery_tasks.main worker -l info -P eventlet
#celery -A celery_tasks.main worker -l info -P eventlet  -c 1000    同时开启1000个协程，提高并发量
