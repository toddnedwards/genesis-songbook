from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.conf import settings
from django.http import HttpResponse
from .models import Category, Product, Order, OrderItem
from .cart import Cart
import stripe
import uuid

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Sorting functionality
    sort = request.GET.get('sort', 'name')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created')
    else:
        products = products.order_by('name')
    
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'current_sort': sort})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'shop/product/detail.html', {'product': product})

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size') if product.is_clothing else None
    
    # Validate size for clothing items
    if product.is_clothing and not size:
        messages.error(request, f'Please select a size for {product.name}')
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('shop:product_list')
    
    cart.add(product=product, quantity=quantity, size=size)
    
    size_text = f" (Size {size})" if size else ""
    messages.success(request, f'{product.name}{size_text} added to cart! ({len(cart)} items total)')
    
    # Get the referring page or default to product list
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('shop:product_list')

@require_POST 
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get('size')
    cart.remove(product, size=size)
    
    size_text = f" (Size {size})" if size else ""
    messages.success(request, f'{product.name}{size_text} removed from cart!')
    return redirect('shop:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart/detail.html', {'cart': cart})

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            address=request.POST['address'],
            postal_code=request.POST['postal_code'],
            city=request.POST['city'],
            country=request.POST.get('country', 'United Kingdom')
        )
        
        # Create order items
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'],
                size=item.get('size')  # Include size if present
            )
        
        # Store order in session
        request.session['order_id'] = order.id
        
        # Clear cart
        cart.clear()
        
        # Redirect to payment
        payment_method = request.POST.get('payment_method', 'stripe')
        if payment_method == 'paypal':
            return redirect('shop:paypal_payment')
        else:
            return redirect('shop:stripe_payment')
            
    return render(request, 'shop/orders/create.html', {'cart': cart})

def stripe_payment(request):
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('shop:product_list')
        
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        # Process Stripe payment here
        # This would integrate with Stripe API
        order.paid = True
        order.payment_status = 'completed'
        order.payment_method = 'stripe'
        order.stripe_id = request.POST.get('stripe_payment_intent_id', '')
        order.save()
        
        messages.success(request, 'Payment successful! Your order has been processed.')
        return redirect('shop:payment_done')
    
    # Create Stripe payment intent
    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=int(order.get_total_cost() * 100),  # Convert to pence
        currency='gbp',
        metadata={'order_id': order.id}
    )
    
    return render(request, 'shop/payment/stripe.html', {
        'order': order,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret
    })

def paypal_payment(request):
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('shop:product_list')
        
    order = get_object_or_404(Order, id=order_id)
    
    return render(request, 'shop/payment/paypal.html', {'order': order})

def payment_done(request):
    return render(request, 'shop/payment/done.html')

def payment_cancelled(request):
    return render(request, 'shop/payment/cancelled.html')
