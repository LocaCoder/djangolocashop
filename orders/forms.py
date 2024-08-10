# django
from django import forms


# local

# Third-party

class CouponApplyForm(forms.Form):
    code = forms.CharField()
