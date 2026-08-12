# shop/forms.py
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_address', 'customer_phone']
        labels = {
            'customer_name': 'お名前',
            'customer_address': 'ご住所',
            'customer_phone': '電話番号',
        }
