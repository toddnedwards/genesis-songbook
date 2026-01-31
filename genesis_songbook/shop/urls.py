from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.order_create, name='order_create'),
    path('payment/stripe/', views.stripe_payment, name='stripe_payment'),
    path('payment/paypal/', views.paypal_payment, name='paypal_payment'),
    path('payment/done/', views.payment_done, name='payment_done'),
    path('payment/cancelled/', views.payment_cancelled, name='payment_cancelled'),
]