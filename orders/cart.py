from main.models import Subscription

CART_SESSION_ID = 'subscription_cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        subscription_ids = self.cart.keys()
        subscription = Subscription.objects.filter(id__in=subscription_ids)
        cart = self.cart.copy()

        for sub in subscription:
            cart[str(sub.id)]['sub_time'] = sub.sub_time_select
            cart[str(sub.id)]['subscription'] = sub
        for item in cart.values():
            item['total_price'] = int(item['price'])
            yield item

    def __len__(self):
        return sum(int(item) for item in self.cart.keys())

    def add(self, subscription):
        subscription_id = str(subscription.id)
        if subscription_id not in self.cart:
            self.cart[subscription_id] = {'price': str(subscription.price)}
        self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        if self.cart:
            del self.session[CART_SESSION_ID]
        self.save()
