from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index.html$',views.index, name='index'),
    url(r'^index$',views.index, name='index'),
    url(r'^login$',views.login,name='login'),
    url(r'^register\.html$', views.register, name="register"),
    url(r'^user-create$',views.user_create,name='user-create'),
    url(r'^customer-orders\.html$', views.customer_home, name='customer-orders'),
    url(r'^customer-account\.html$', views.customer_view, name='acc_detail'),
    url(r'^customer-order\.html/([0-9]*)$',views.order_detail, name='order-detail'),
    url(r'^logout$',views.logout, name='logout'),
    url(r'^category\.html/([0-9]*)$',views.cat_view, name='cat-view'),
    url(r'^detail\.html/([0-9]*)$',views.prod_view, name='prod-view'),
    url(r'^cart$',views.cart_addproduct, name='cart-add'),
    url(r'^update_cart$',views.update_cart,name='cart-update'),
    url(r'^cart-del/([0-9]*)$',views.cart_delproduct, name='cart-del'),
    url(r'^basket\.html$',views.cart, name='cart-view'),
    url(r'^basket\.html/([0-9]*)$',views.cart_defadd, name='cart-view'),
    url(r'^checkout1\.html$',views.checkout1, name='cart-view'),
    url(r'^checkout2\.html$',views.checkout2, name='cart-view'),
    url(r'^checkout3\.html$',views.checkout3, name='cart-view'),
    url(r'^checkout4\.html$',views.checkout4, name='cart-view'),
    url(r'^order$',views.order,name="complete-order"),
    url(r'^search$',views.search,name="search"),
    url(r'^blog\.html$',views.blog,name="iwegfi"),
    url(r'^review$',views.reviews,name='reviews '),
    url(r'^404$',views.four_04, name='not_found'),
    url(r'^contact\.html$',views.contact, name='contact-us'),
    url(r'^faq\.html$',views.faq, name='faq'),
    url(r'^text\.html$',views.text, name='text-page'),
    url(r'^post\.html$',views.post, name='post-blog')
]
