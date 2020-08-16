from django.conf.urls import url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from .views import statistical,users,specs,images,skus,orders,permissions,group,admin
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # 登录
    url(r'^authorizations/$', obtain_jwt_token),
    # --------------  数据统计 -----------------
    # 用户总量
    url(r'^statistical/total_count/$', statistical.UserCountView.as_view()),
    # 日增用户
    url(r'^statistical/day_increment/$', statistical.UserDayCountView.as_view()),
    # 日活用户
    url(r'^statistical/day_active/$', statistical.UserDayActiveCountView.as_view()),
    # 下单用户
    url(r'^statistical/day_orders/$', statistical.UserDayOrdersCountView.as_view()),
    # 月增用户
    url(r'^statistical/month_increment/$', statistical.UserMonthCountView.as_view()),

    url(r'^statistical/goods_day_views/$', statistical.UserGoodsCountView.as_view()),
    # ------------- 用户管理路由--------------
    url(r'^users/$', users.UserView.as_view()),

    # ------------规格路由表-----------
    url(r'^goods/simple/$', specs.SpecsView.as_view({'get': 'simple'})),

    # ------------图片路由————————————
    url(r'^skus/simple/$', images.ImagesView.as_view({'get': 'simple'})),

    # ------------sku路由————————————
    url(r'^goods/(?P<pk>\d+)/specs/$', skus.SKUVIew.as_view({'get': 'specs'})),

    # --------权限路由--------
    url(r'^permission/content_types/$', permissions.PermissionsView.as_view({'get': 'content_type'})),

    url(r'^permission/simple/$', group.GroupView.as_view({'get': 'simple'})),

    url(r'^permission/groups/simple/$', admin.AdminView.as_view({'get': 'simple'})),

]

# ----------规格表路由------
router = DefaultRouter()
router.register('goods/specs', specs.SpecsView, base_name='specs')
print(router.urls)
urlpatterns += router.urls

# -------图片表路由------
router = DefaultRouter()
router.register('skus/images', images.ImagesView, base_name='images')
print(router.urls)
urlpatterns += router.urls

# --------sku路由--------
router = DefaultRouter()
router.register('skus', skus.SKUVIew, base_name='images')
print(router.urls)
urlpatterns += router.urls

# --------订单路由--------
router = DefaultRouter()
router.register('orders', orders.OrderView, base_name='orders')
print(router.urls)
urlpatterns += router.urls


# --------权限路由--------
router = DefaultRouter()
router.register('permission/perms', permissions.PermissionsView, base_name='perms')

urlpatterns += router.urls


# --------分组路由--------
router = DefaultRouter()
router.register('permission/groups', group.GroupView, base_name='groups')
print(router.urls)
urlpatterns += router.urls


# --------管理员路由--------
router = DefaultRouter()
router.register('permission/admins',admin.AdminView, base_name='admin')
print(router.urls)
urlpatterns += router.urls



