from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
def home_view(request):
    products = Product.objects.all()
    cart = request.session.get('cart', [])

    return render(request, 'home.html', {
        'products': products,
        'cart_count': len(cart)
    })

def item_details(request, product_id):
    product = get_object_or_404(Product, id=product_id, availability=True)

    cart = request.session.get('cart', [])

    return render(request, 'item_details.html', {
        'product': product,
        'cart_count': len(cart)
    })

def add_to_cart(request, product_id):
    if request.method == "POST":

        cart = request.session.get('cart', {})

        product_id = str(product_id)

        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1

        request.session['cart'] = cart

        return JsonResponse({
            'success': True,
            'cart_count': sum(cart.values())
        })

    return redirect('home')

    return redirect('home')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')

def cart(request):

    cart_data = request.session.get('cart', {})

    products = []

    total = 0

    for product_id, quantity in cart_data.items():

        product = Product.objects.get(id=product_id)

        subtotal = product.price * quantity

        total += subtotal

        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {
        'products': products,
        'total': total,
        'cart_count': sum(cart_data.values())
    })

def increase_quantity(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session['cart'] = cart

    return redirect('cart')

def decrease_quantity(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:

        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')

def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True

    return redirect('cart')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']

            user.save()

            login(request, user)

            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def panel_view(request):
    cart = request.session.get('cart', {})

    if isinstance(cart, dict):
        cart_count = sum(cart.values())
    else:
        cart_count = len(cart)

    return render(request, 'panel.html', {
        'cart_count': cart_count
    })

def get_cart_count(request):
    cart = request.session.get('cart', {})

    if isinstance(cart, dict):
        return sum(cart.values())

    return len(cart)

def kontakt_view(request):
    cart = request.session.get('cart', [])

    return render(request, 'kontakt.html', {
        'cart_count': len(cart)
    })

def check_username(request):
    username = request.GET.get('username', '')

    exists = User.objects.filter(username=username).exists()

    return JsonResponse({
        'exists': exists
    })

@login_required
def user_data_view(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values()) if isinstance(cart, dict) else len(cart)

    if request.method == "POST":
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()

        return redirect('user_data')

    return render(request, 'user_data.html', {
        'cart_count': cart_count
    })


@login_required
def user_orders_view(request):
    return render(request, 'user_orders.html', {
        'cart_count': get_cart_count(request)
    })


@login_required
def user_favorites_view(request):
    return render(request, 'user_favorites.html', {
        'cart_count': get_cart_count(request)
    })


@login_required
def user_addresses_view(request):
    return render(request, 'user_addresses.html', {
        'cart_count': get_cart_count(request)
    })

@login_required
def user_settings_view(request):
    return render(request, 'user_settings.html', {
        'cart_count': get_cart_count(request)
    })
   