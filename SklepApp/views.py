from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, Order, OrderItem, Address
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

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
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        if not User.objects.filter(username=username).exists():
            messages.error(
                request,
                "Nie istnieje użytkownik o takiej nazwie."
            )
        else:
            messages.error(
                request,
                "Błędne hasło."
            )

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        email = request.POST.get('email')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Konto z takim adresem e-mail już istnieje.")
            return render(request, 'register.html', {'form': form})
        
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
    cart_count = get_cart_count(request)

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")[:3]

    orders_count = Order.objects.filter(
        user=request.user
    ).count()

    return render(request, 'panel.html', {
        'cart_count': cart_count,
        'orders': orders,
        'orders_count': orders_count
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
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, 'user_orders.html', {
        'orders': orders,
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
   
def forgot_password_view(request):

    if request.method == "POST":

        messages.success(
            request,
            "Jeżeli konto istnieje, wysłaliśmy instrukcję resetu hasła."
        )

    return render(request, 'forgot_password.html')

@login_required
def checkout_view(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    address = Address.objects.filter(user=request.user).first()

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        street = request.POST.get("street")
        postal_code = request.POST.get("postal_code")
        city = request.POST.get("city")

        total = 0
        order_items = []

        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            subtotal = product.price * quantity
            total += subtotal

            order_items.append({
                "product": product,
                "quantity": quantity,
                "price": product.price
            })

        order = Order.objects.create(
            user=request.user,
            total=total,
            full_name=full_name,
            phone=phone,
            street=street,
            postal_code=postal_code,
            city=city
        )

        for item in order_items:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["price"]
            )

        request.session["cart"] = {}
        request.session.modified = True

        return redirect("order_success", order_id=order.id)

    return render(request, "checkout.html", {
        "address": address
    })


@login_required
def order_success_view(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    return render(request, 'order_success.html', {
        'order': order
    })

@login_required
def order_detail_view(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    return render(request, 'order_detail.html', {
        'order': order,
        'cart_count': get_cart_count(request)
    })