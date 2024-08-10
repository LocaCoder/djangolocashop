from kavenegar import *
from django.contrib.auth.mixins import UserPassesTestMixin


def send_otp_code(phone_number, code):
    pass
    # try:
    #     api = KavenegarAPI('7575654577353553724C7A5666382B506873573639674463566F7151303361474C675A4C6E322F304232383D')
    #     params = {
    #         'sender' : '',
    #         'receptor' : phone_number,
    #         'message' : f'{code} کد تایید شما :'
    #     }
    #     response = api.sms_send(params)
    #     print(response)
    # except APIException as e:
    #     print(e)
    # except HTTPException as e:
    #     print(e)


class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin
