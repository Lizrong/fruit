from django.urls import path, include, re_path

from axf import views
from axf.views import *
app_name='axf'
urlpatterns = [

    re_path(r'^home/$',views.home,name='home'),
    re_path(r'^market/(\d+)/(\d+)/(\d)/$',views.market, name='market'),

    re_path(r'^mine/$', views.mine, name='mine'),
    re_path(r'^checkusername/$',check_username),
    re_path(r'^userreg/$',user_register,name='userreg'),
    re_path(r'^userlogin/$',user_login,name='userlogin'),
    re_path(r'^userdetail/$',user_detail,name='userdetail'),
    re_path(r'^quit/$', quit, name='quit'),

    re_path(r'^cart/$', views.cart, name='cart'),
    re_path(r'^addtocart/$',add_to_cart),
    re_path(r'^subtocart/$',sub_to_cart),

    re_path(r'^changeselect/$',change_cart_select),
    re_path(r'^changeallselect/$',change_all_select),
]
