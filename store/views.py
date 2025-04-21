from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Wishlist
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(available=True)[:8]
    context = {
        'categories': categories,
        'featured_products': featured_products
    }
    return render(request, 'store/home.html', context)

def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, available=True)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'store/category_products.html', context)

def new_arrivals(request):
    # Get products created in the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    products = Product.objects.filter(
        available=True, 
        created_at__gte=thirty_days_ago
    ).order_by('-created_at')
    
    context = {
        'products': products,
        'title': 'New Arrivals',
    }
    return render(request, 'store/new_arrivals.html', context)

def sale(request):
    # For demonstration purposes, we'll assume products with price < 2000 are on sale
    # In a real app, you'd have a discount field or a specific QuerySet based on your model
    products = Product.objects.filter(
        available=True,
        price__lt=2000
    ).order_by('price')
    
    # Add a fake discount percentage for display purposes
    for product in products:
        # Just for demonstration - in a real app, you'd use actual discount values
        if product.price < 1000:
            product.discount = 50
        elif product.price < 1500:
            product.discount = 40
        else:
            product.discount = 30
        
        # Calculate original price for display (just for demonstration)
        # Convert float to Decimal to avoid type mismatch
        discount_factor = Decimal(100.0 / (100 - product.discount))
        product.original_price = product.price * discount_factor
    
    context = {
        'products': products,
        'title': 'Sale',
    }
    return render(request, 'store/sale.html', context)

def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, available=True)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'store/product_detail.html', context)

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart
    }
    return render(request, 'store/cart_detail.html', context)

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, 'Product added to cart successfully.')
    return redirect('store:cart_detail')

@login_required
def cart_remove(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        messages.success(request, 'Cart updated successfully.')
    except CartItem.DoesNotExist:
        messages.error(request, 'Product not found in cart.')
    
    return redirect('store:cart_detail')

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'store/order_list.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order
    }
    return render(request, 'store/order_detail.html', context)

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        
        if not address or not phone:
            messages.error(request, 'Please provide both address and phone number.')
            return redirect('store:checkout')
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            address=address,
            phone=phone,
            total_amount=cart.total
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        
        # Clear cart
        cart.items.all().delete()
        
        messages.success(request, 'Order placed successfully!')
        return redirect('store:order_detail', order_id=order.id)
    
    context = {
        'cart': cart
    }
    return render(request, 'store/checkout.html', context)

@login_required
def wishlist_detail(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist': wishlist})

@login_required
def wishlist_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        if is_ajax:
            return JsonResponse({'status': 'removed', 'message': 'Product removed from wishlist'})
        messages.success(request, 'Product removed from wishlist.')
    else:
        wishlist.products.add(product)
        if is_ajax:
            return JsonResponse({'status': 'added', 'message': 'Product added to wishlist'})
        messages.success(request, 'Product added to wishlist.')
    
    # Redirect to the referring page or wishlist page
    if is_ajax:
        return JsonResponse({'status': 'error', 'message': 'Something went wrong'})
    
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('store:wishlist_detail')

@login_required
def wishlist_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.success(request, 'Product removed from wishlist.')
    
    return redirect('store:wishlist_detail')