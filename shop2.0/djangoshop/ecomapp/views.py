from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from ecomapp.models import Category, Product, CartItem, Cart

def base_view(request):
	cart = cart_create(request)
	categories=Category.objects.all()
	products=Product.objects.all()
	context={
		'categories':categories,
		'products':products,
		'cart': cart
		
	}

	return render(request,'base.html', context)


def product_view(request, product_slug):
	cart = cart_create(request)
	product = Product.objects.get(slug = product_slug)
	categories=Category.objects.all()
	context = {
		'product': product,
		'categories':categories,
		'cart': cart
	}
	return render(request, 'product.html', context)

def category_view(request, category_slug):
	cart = cart_create(request)
	category = Category.objects.get(slug = category_slug)
	products_of_category = Product.objects.filter(category = category)
	categories=Category.objects.all()
	context = {
		'category': category,
		'products_of_category': products_of_category,
		'categories':categories,
		'cart': cart
	}
	return render(request, 'category.html', context)


def cart_view(request):
	cart = cart_create(request)
	context = {
		'cart': cart
	}
	return render(request, 'cart.html', context)


def add_to_cart_view(request, product_slug):
	product = Product.objects.get(slug = product_slug)
	cart = cart_create(request)
	cart.add_to_cart(product.slug)
	return HttpResponseRedirect(reverse('cart'))


def remove_from_cart_view(request, product_slug):
	product = Product.objects.get(slug = product_slug)
	cart = cart_create(request)
	cart.remove_from_cart(product.slug)
	return HttpResponseRedirect(reverse('cart'))



def cart_create(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total']=cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    return cart