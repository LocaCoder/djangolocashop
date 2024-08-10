from django.urls import path
from . import views

app_name = 'orders'


urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart_view'),
    path('cart/add/<int:subscription_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('detail/<int:order_id>', views.OrederDetailView.as_view(), name='order_detail'),
    path('apply/<int:order_id>', views.CouponApplyView.as_view(), name='apply_coupon'),
    # path('request/', views.OrderSendRequest.as_view(), name='request'),
    # path('verify/', views.OrderVerify.as_view(), name='verify'),
]