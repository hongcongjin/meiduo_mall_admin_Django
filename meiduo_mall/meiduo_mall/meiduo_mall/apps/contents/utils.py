from collections import OrderedDict

from goods.models import GoodsChannel


def get_categories():
    """获取商品分类"""
    # 准备商品分类对应的字典
    categories = OrderedDict()
    # 查询所有的商品频道:37个一级类别
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    # 遍历所有频道
    for channel in channels:
        # 获取当前频道所在的组
        group_id = channel.group_id
        # 构造基本的数据框架:只有11个组
        if group_id not in categories:
            categories[group_id] = {'channels': [], 'sub_cats': []}

        # 查询当前频道对应的一级类别
        cat1 = channel.category
        # 将cat1添加到channels
        categories[group_id]['channels'].append({
            'id': cat1.id,
            'name': cat1.name,
            'url': channel.url
        })

        # 查询二级和三级类别
        for cat2 in cat1.subs.all():  # 从一级类别找二级类别
            cat2.sub_cats = []  # 给二级类别添加一个保存三级类别的列表
            for cat3 in cat2.subs.all():  # 从二级类别找三级类别
                cat2.sub_cats.append(cat3)  # 将三级类别添加到二级sub_cats

            # 将二级类别添加到一级类别的sub_cats
            categories[group_id]['sub_cats'].append(cat2)
    return categories