from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from .models import Product, Cart, CartItem, UserProfile
from .forms import AddToCartForm, RegistrationForm, ProductForm
from django.contrib import messages
from django.urls import reverse

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('parts_store:login_view')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def user_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    cart, created_cart = Cart.objects.get_or_create(user_profile=user_profile)

    return render(request, 'user_profile.html', {'user_profile': user_profile, 'cart': cart})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('parts_store:product_list')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def register_view(request):
    return render(request, 'registration/register.html')

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    user_profile = request.user.userprofile
    cart, created = Cart.objects.get_or_create(user_profile=user_profile)


    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)


    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('parts_store:product_list')

@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return redirect('user_profile')

@login_required
def view_cart(request):
    user_profile = request.user.userprofile
    cart = Cart.objects.get_or_create(user_profile=user_profile)[0]
    return render(request, 'view_cart.html', {'cart': cart})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('parts_store:product_list')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

def about(request):
    return render(request, 'about.html')
