def get_breadcrumb(cat3):
    # 面包屑导航
    cat2 = cat3.parent
    cat1 = cat2.parent
    breadcrumb = {
        'cat1': {
            'url': cat1.channels.all()[0].url,
            'name': cat1.name
        },
        'cat2': cat2,
        'cat3': cat3,
    }
    return breadcrumb
