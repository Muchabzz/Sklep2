from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product
from django.contrib.auth.decorators import login_required

# Create your views here.
def home_view(request):
    products = Product.objects.filter(availability=True)
    return render(request, 'home.html', {'products': products})

def item_details(request, product_id):
    product = get_object_or_404(Product, id=product_id, availability=True)
    return render(request, 'item_details.html', {'product': product})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])

    if product_id not in cart:
        cart.append(product_id)

    request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])

    if product_id in cart:
        cart.remove(product_id)

    request.session['cart'] = cart
    return redirect('cart')

def cart(request):
    cart_ids = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart_ids)

    total = sum(product.price for product in products)

    return render(request, 'cart.html', {
        'products': products,
        'total': total
    })

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
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def panel_view(request):
    return render(request, 'panel.html')

def kontakt_view(request):
    return render(request, 'kontakt.html')