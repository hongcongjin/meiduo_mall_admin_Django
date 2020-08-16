from django.shortcuts import render
from django.views import View
from collections import OrderedDict

from contents.models import ContentCategory
from contents.utils import get_categories
# Create your views here.


class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告页面"""
        # 查询并展示商品分类
        categories = get_categories()

        # 查询首页广告数据
        # 查询所有的广告类别
        contents = OrderedDict()
        content_categories = ContentCategory.objects.all()
        for content_category in content_categories:
            # 使用广告类别查询出该类别对应的所有的广告内容
            contents[content_category.key] = content_category.content_set.filter(status=True).order_by('sequence') # 查询出未下架的广告并排序

        # 构造上下文
        context = {
            'categories':categories,
            'contents':contents
        }

        return render(request, 'index.html', context)