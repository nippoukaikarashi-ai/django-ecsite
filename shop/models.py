from django.db import models
from django.conf import settings

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)                     #商品名が最大百文字の文字列で入る
    price = models.IntegerField()                               #整数の価格が入るよ
    description = models.TextField()                            #長い文書でも商品説明できるよ
    stock = models.IntegerField(default=0)                      #初期値0の在庫数
    created_at = models.DateTimeField(auto_now_add=True)        #作成日時自動で現在日時が記録される

class Order(models.Model):
    #顧客情報
    customer_name = models.CharField("氏名", max_length=100)
    customer_address = models.CharField("住所", max_length=255)
    customer_phone = models.CharField("電話番号", max_length=20)

    # 注文ステータス
    STATUS_CHOICES = [
        ('awaiting_payment', '支払待ち'),
        ('paid', '入金済み'),
        ('shipped', '発送済み'),
    ]

    status = models.CharField("ステータス", max_length=20, choices=STATUS_CHOICES, default='awaiting_payment')

    #金額と日時
    total_price = models.PositiveIntegerField("合計金額")
    created_at = models.DateTimeField("注文日時", auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField("数量")
    price = models.PositiveIntegerField("単価")

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

def _str_(self):
    return self.name

class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=128)
