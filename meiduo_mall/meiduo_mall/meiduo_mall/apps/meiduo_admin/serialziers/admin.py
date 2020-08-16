from rest_framework import serializers
from users.models import User


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        # 给字段增加额外参数
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    # 父类保存数据库的方法不满足需求，重写方法
    def create(self, validated_data):
        user = super().create(validated_data)
        user.is_staff = True
        # 密码加密set_password
        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        # 密码加密set_password
        user.set_password(validated_data['password'])
        user.save()
        return user
