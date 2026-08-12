from django.urls import path
from . import views                     #同じディレクトリにある viwes.pyをインポート

app_name = 'shop'

urlpatterns = [
    # 商品一覧　path(URLのパターン, 呼び出すビュー関数, name=URLの名前)
    path('', views.product_list, name='product_list'),

    #商品詳細ページ
    path('<int:pk>/', views.product_detail, name='product_detail'),

    #カート機能
    path('add/<int:pk>/', views.add_to_cart, name='add_to_cart'),

    #カート確認機能
    path('cart/', views.cart_detail, name='cart_detail'),

    #カート削除機能
    path('remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),

    #カート数量更新機能
    path('cart/update/', views.update_cart, name='update_cart'),

    #銀行口座関係
    path('checkout/', views.checkout, name='checkout'),

]
