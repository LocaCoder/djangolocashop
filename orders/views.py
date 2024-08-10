# django
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.conf import settings
# local
from .models import Subscription, Order, OrderItem, Coupon
from .forms import CouponApplyForm
from .cart import Cart
# Third-party
import requests
import json
import datetime


# Create your views here.
class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})


class CartAddView(LoginRequiredMixin, View):
    def post(self, request, subscription_id):
        cart = Cart(request)
        subscription = get_object_or_404(Subscription, id=subscription_id)

        cart.add(subscription)
        return redirect('orders:cart_view')


class OrederDetailView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/order.html', {'order': order, 'form': self.form_class})


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, subscription=item['subscription'], price=item['price'])
        cart.clear()
        return redirect('orders:order_detail', order.id)


class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def post(self, request, order_id):
        now = datetime.datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_form__lte=now, valid_to__gte=now,
                                            active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'This coupon dose not exists')
                return redirect('orders:order_detail', order_id)
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
            return redirect('orders:order_detail', order_id)

#
# # ? sandbox merchant
# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'
#
# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
#
# amount = 1000  # Rial / Required
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# phone = 'YOUR_PHONE_NUMBER'  # Optional
# # Important: need to edit for realy server.
# CallbackURL = 'http://127.0.0.1:8080/verify/'
#

# class OrderSendRequest(View):
#     data = {
#         "MerchantID": settings.MERCHANT,
#         "Amount": amount,
#         "Description": description,
#         "Phone": phone,
#         "CallbackURL": CallbackURL,
#     }
#     data = json.dumps(data)
#     # set content length by data
#     headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#     try:
#         response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
#
#         if response.status_code == 200:
#             response = response.json()
#             if response['Status'] == 100:
#                 return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
#                         'authority': response['Authority']}
#             else:
#                 return {'status': False, 'code': str(response['Status'])}
#         return response
#
#     except requests.exceptions.Timeout:
#         return {'status': False, 'code': 'timeout'}
#     except requests.exceptions.ConnectionError:
#         return {'status': False, 'code': 'connection error'}
#
#
# class OrderVerify(View):
#     def get(self, order_id):
#         order = Order.objects.filter(id=order_id)
#         data = {
#             "MerchantID": settings.MERCHANT,
#             "Amount": order.,
#             "Authority": authority,
#         }
#         data = json.dumps(data)
#         # set content length by data
#         headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#         response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
#
#         if response.status_code == 200:
#             response = response.json()
#             if response['Status'] == 100:
#                 return {'status': True, 'RefID': response['RefID']}
#             else:
#                 return {'status': False, 'code': str(response['Status'])}
#         return response
