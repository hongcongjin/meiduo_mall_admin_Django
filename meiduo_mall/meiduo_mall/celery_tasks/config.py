# Celery配置文件

# 指定中间人、消息队列、任务队列、容器，使用redis
broker_url = "redis://127.0.0.1:6379/11"




#启动celery异步命令
#celery -A celery_tasks.main worker -l info -P eventlet