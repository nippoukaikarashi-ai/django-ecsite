from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from .models import Product, Order, OrderItem
from .forms import OrderForm
import uuid

def product_list(request):
    products = products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'shop/product_list.html', context)

# 商品詳細 (この関数を新しく追加)
def product_detail(request, pk):
    # pkを元に、データベースから商品を一つだけ取得
    # もし商品が見つからなければ、404エラー出る
    product = get_object_or_404(Product, pk=pk)

    # 2. 取得した商品をテンプレートに渡して、htmlを生成
    context = {
        'product': product,
    }
    return render(request, 'shop/product_detail.html', context)

def add_to_cart(request, pk):
    # セッションからカートの情報を取得する (無ければ空の辞書)
    cart = request.session.get('cart', {})

    # カートに商品を追加する(キーは商品ID、値は数量)
    # すでに商品があれば数量を1増やし、無ければ数量を1として追加
    cart[str(pk)] = cart.get(str(pk), 0) + 1

    # 更新したカートの情報をセッションに保存する
    request.session['cart'] = cart

    # 商品一覧ページにリダイレクトする
    return redirect('shop:product_list')

def cart_detail(request):
    #1.セッションからカートの情報を取得する
    cart = request.session.get('cart', {})

    #2. カート情報を元に、表示用の商品リストを作成する
    cart_items = []
    total_price = 0
    product_ids =cart.keys()  # カートに入っている商品のIDリストを作成する

    if product_ids:
        # 3. IDリストを使って、必要な商品情報を一括でDBから取得
        products = Product.objects.filter(pk__in=product_ids)

        for product in products:
            quantity = cart[str(product.pk)]
            subtotal = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })
            total_price += subtotal

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }

        return render(request, 'shop/cart_detail.html', context)

def remove_from_cart(request, pk):
    # 1. セッションからカートの情報を取得する
    cart = request.session.get('cart', {})

    # 2. 削除対象の商品IDがカートにあれば、その商品を削除する
    #  辞書のキーは文字列なので、pkも文字列に変換してチェックする
    if str(pk) in cart:
        del cart[str(pk)]

    # 3. 更新したカートの情報を元にセッションに保存する
    request.session['cart'] = cart

    # 4. カート詳細ページにリダイレクトする
    return redirect('shop:cart_detail')

def update_cart(request):

    # 1. POSTリクエスト出なければ何もしない
    if  request.method == 'POST':

        # 2.  セッションからカートの情報を取得する
        cart = request.session.get('cart', {})

        # 3. フォームから送信された各商品の情報をループだけで処理
        for key, value in request.POST.items():

            # 4.キーが'quantity_'で始まるものだけを処理
            if key.startswith('quantity_'):

                # 5.商品IDと新しい数量を取得
                product_id = key.split('_')[1]
                try:
                    new_quantity = int(value)
                except ValueError:
                    continue #数字でなければスキップ

                # 6. カート内の情報を更新
                if product_id in cart:
                    if new_quantity > 0:
                        cart[product_id] = new_quantity
                    else:
                        del cart[product_id]

        # 7.更新したカート情報をセッションに保存
        request.session['cart'] = cart

    # 8.カート詳細ページにリダイレクト
    return redirect('shop:cart_detail')

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        # カートが空ならカートページにリダイレクト
        return redirect('shop:cart_detail')

    # カートの中身と合計金額を計算 (cart_detailビューのロジックを再利用)
    cart_items = []
    total_price = 0
    products = Product.objects.filter(pk__in=cart.keys())
    for product in products:
        quantity = cart[str(product.pk)]
        subtotal = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total_price += subtotal
    
    # POSTリクエストの場合（フォームが送信された場合）
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                # 安全なデータ保存（もし途中で失敗したら全て元に戻す）
                with transaction.atomic():
                    # 1. 注文情報（Order）を保存
                    order = form.save(commit=False)
                    order.total_price = total_price
                    order.save()
                    
                    # 2. 注文明細（OrderItem）を保存
                    for item in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            product=item['product'],
                            quantity=item['quantity'],
                            price=item['product'].price
                        )

                # 3. カートを空にする
                del request.session['cart']
                
                # 4. 注文完了ページにリダイレクト（将来的には完了ページを作る）
                # ここでは仮に商品一覧ページに戻る
                return redirect('shop:product_list')

            except Exception as e:
                # TODO: エラーハンドリング
                print(e) # 開発中はエラー内容をコンソールに出力
    
    # GETリクエストの場合（ページを最初に表示する場合）
    else:
        form = OrderForm()

    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'shop/checkout.html', context)
