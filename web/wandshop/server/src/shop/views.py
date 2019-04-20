from decimal import Decimal

from django.shortcuts import render, redirect
from shop.models import Item


def calculate_remaining_coins(request):
    cur = Decimal(1337)
    for x in request.session.get('cart', []):
        cur -= Decimal(x['price'])
    return cur

def has_won(request):
    for x in request.session.get('cart', []):
        if x['sku'] == '321':
            return True
    return False

def handle_action(request):
    action = request.POST.get('action')
    if action == 'add_cart':
        item_sku = request.POST.get('sku')
        price = request.POST.get('price')
        amount = calculate_remaining_coins(request)
        if Decimal(price) > amount:
            request.session['error'] = "Not enough credit!"
            return redirect("/")
        if request.session.get('cart') is None:
            request.session['cart'] = []
        cart = request.session['cart']
        cart.append({'sku': item_sku, 'price': price})
        request.session['cart'] = cart
    if action == 'reset':
        request.session['cart'] = []

    if action == 'order':
        if has_won(request):
            return render(request, 'shop/flag.html')
        else:
            return render(request, 'shop/order.html')

    return redirect("/")


# Create your views here.
def index(request):
    print(request.method)
    if request.method == 'POST':
        return handle_action(request)

    template_params = {
        'items': Item.objects.all(),
        'coins': str(calculate_remaining_coins(request)),
        'cart': request.session.get('cart', []),
        'error': request.session.get('error')
    }

    request.session['error'] = None

    items = Item.objects.all()
    return render(request, 'shop/index.html', template_params)
