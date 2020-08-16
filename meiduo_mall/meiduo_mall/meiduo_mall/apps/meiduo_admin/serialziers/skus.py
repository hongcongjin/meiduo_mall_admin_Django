from rest_framework import serializers
from django.db import transaction
from celery_tasks.static_file.tasks import get_detail_html

from goods.models import SKU, GoodsCategory, SPUSpecification, SpecificationOption, SKUSpecification


class SKUSpecificationSerializer(serializers.ModelSerializer):
    """
            sku具体规格表数据
    """
    spec_id = serializers.IntegerField()
    option_id = serializers.IntegerField()

    class Meta:
        model = SKUSpecification
        fields = ('spec_id', 'option_id')


class SKUSerialzier(serializers.ModelSerializer):
    """
        sku序列化器
    """
    spu_id = serializers.IntegerField()
    category_id = serializers.IntegerField()

    # specificationoption_set {}.spec_id
    specs = SKUSpecificationSerializer(read_only=True, many=True)

    class Meta:
        model = SKU
        fields = "__all__"
        read_only_fields = ('spu', 'category')

    # @transaction.atomic()
    def create(self, validated_data):
        specs = self.context['request'].data.get('specs')
        # 开启事务
        with transaction.atomic():
            # 设置保存点
            save_point = transaction.savepoint()
            try:
                # 保存sku表
                sku = SKU.objects.create(**validated_data)
                # 保存sku具体规格表
                for spec in specs:
                    SKUSpecification.objects.create(spec_id=spec['spec_id'], option_id=spec['option_id'], sku=sku)

            except:
                # 回滚
                transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError('保存失败')

            else:
                # 提交
                transaction.savepoint_commit(save_point)

                # 生成详情页的静态页面
                get_detail_html.delay(sku.id)

                return sku

    def update(self, instance, validated_data):
        specs = self.context['request'].data.get('specs')
        # 开启事务
        with transaction.atomic():
            # 设置保存点
            save_point = transaction.savepoint()
            try:
                # 修改sku表
                SKU.objects.filter(id=instance.id).update(**validated_data)
                # 修改sku具体规格表
                for spec in specs:
                    SKUSpecification.objects.filter(sku=instance).update(**spec)

            except:
                # 回滚
                transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError('保存失败')

            else:
                # 提交
                transaction.savepoint_commit(save_point)

                # 生成详情页的静态页面
                get_detail_html.delay(instance.id)

                return instance


class GoodsCategorySerializer(serializers.ModelSerializer):
    """
        商品分类序列化器
    """

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class SpecificationOptionSerializer(serializers.ModelSerializer):
    # SPU规格序选项列化器
    class Meta:
        model = SpecificationOption
        fields = '__all__'


class SPUSpecificationSerializer(serializers.ModelSerializer):
    """
        SPU规格序列化器
    """
    options = SpecificationOptionSerializer(many=True)

    # specificationoption_set=SpecificationOption(many=True)

    class Meta:
        model = SPUSpecification
        fields = '__all__'
