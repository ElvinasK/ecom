from django.shortcuts import render, redirect
from .models import Product, Category, Profile , ShippingOrder, OrderItem
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm, PaymentForm
from django import forms
from django.db.models import Q
from cart.cart import Cart
import datetime

def orders(request, pk):
	if request.user.is_authenticated and request.user.is_superuser:
		# Get the order
		order = ShippingOrder.objects.get(id=pk)
		# Get the order items
		items = OrderItem.objects.filter(order=pk)

		if request.POST:
			status = request.POST['shipping_status']
			# Check if true or false
			if status == "true":
				# Get the order
				order = ShippingOrder.objects.filter(id=pk)
				# Update the status
				now = datetime.datetime.now()
				order.update(shipped=True, date_shipped=now)
			else:
				# Get the order
				order = ShippingOrder.objects.filter(id=pk)
				# Update the status
				order.update(shipped=False)
			messages.success(request, "Shipping Status Updated")
			return redirect('home')


		return render(request, 'orders.html', {"order":order, "items":items})




	else:
		messages.success(request, "Access Denied")
		return redirect('home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = ShippingOrder.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            # Get the order
            order = ShippingOrder.objects.filter(id=num)
            # grab Date and time
            now = datetime.datetime.now()
            # update order
            order.update(shipped=True, date_shipped=now)
            # redirect
            messages.success(request, "Shipping Status Updated")
            return redirect('home')

        return render(request, "not_shipped_dash.html", {"orders": orders})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = ShippingOrder.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            # grab the order
            order = ShippingOrder.objects.filter(id=num)
            # grab Date and time
            now = datetime.datetime.now()
            # update order
            order.update(shipped=False)
            # redirect
            messages.success(request, "Shipping Status Updated")
            return redirect('home')

        return render(request, "shipped_dash.html", {"orders": orders})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # get billing info from the last page
        payment_form = PaymentForm(request.POST or None)
        # get shipping session data
        my_shipping = request.session.get('my_shipping')


        # Gather order info
        full_name = my_shipping['full_name']
        email = my_shipping['shipping_email']

        # Create shipping adress from session info
        shipping_address = f"{my_shipping['address1']}\n{my_shipping['address2']}\n{my_shipping['city']}\n{my_shipping['zipcode']}\n{my_shipping['country']}"
        amount_paid = totals

        # Create order
        if request.user.is_authenticated:
            # logged in
            user = request.user
            create_order = ShippingOrder(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # add order items
            # get the order id
            order_id = create_order.pk

            # get product info
            for product in cart_products():

                # get product id
                product_id = product.id

            #     get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                    # get quantity
                for key, value in quantities().items():
                    if int(key) == product_id:
                        # create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user , quantity=value, price=price)
                        create_order_item.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # delete key
                    del request.session[key]


            messages.success(request, ("Your order has been processed!"))
            return redirect('home')

        else:
            # not logged in
            create_order = ShippingOrder(full_name=full_name, email=email, shipping_address=shipping_address,
                                         amount_paid=amount_paid)
            create_order.save()

            # add order items
            # get the order id
            order_id = create_order.pk

            # get product info
            for product in cart_products():

                # get product id
                product_id = product.id

                #     get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                    # get quantity
                for key, value in quantities().items():
                    if int(key) == product_id:
                        # create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # delete key
                    del request.session[key]


            messages.success(request, ("Your order has been processed!"))
            return redirect('home')


    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Create a session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # check to see if user is logged in
        if request.user.is_authenticated:
            # Get billing form
            billing_form = PaymentForm()
            return render(request, "billing_info.html",
                          {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_info": request.POST, "billing_form": billing_form})
        else:
            # not logged in
            billing_form = PaymentForm()
            return render(request, "billing_info.html",
                          {"cart_products": cart_products, "quantities": quantities, "totals": totals,
                           "shipping_info": request.POST, "billing_form": billing_form})

        form = request.POST
        return render(request, "billing_info.html",
                      {"cart_products": cart_products, "quantities": quantities, "totals": totals, "form": form})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # check outas loggedin user
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        return render(request, "checkout.html",
                      {"cart_products": cart_products, "quantities": quantities, "totals": totals, "form": form})
    else:
        # checkout as guest
        form = UserInfoForm(request.POST or None)
        return render(request, "checkout.html",
                      {"cart_products": cart_products, "quantities": quantities, "totals": totals,"form": form})


def payment_success(request):
    return render(request, 'payment_success.html', {})


def search(request):
    # Determine if they filled out the form
    if request.method == 'POST':
        searched = request.POST['searched']
        # Query The Products DB Model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        # Test for null
        if not searched:
            messages.success(request, ("That Product doesn't exist"))
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html',{'searched':searched} )
    else:
        return render(request, 'search.html', {})

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, ("Your info has been updated!"))
            return redirect('home')
        return render(request, 'update_info.html', {'form': form})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
    #     Did they fill out the form?
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, ("Your password has been updated!"))
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, ("You have login to view this page"))
        return redirect('home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, ("Your account has been updated!"))
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories":categories})
def category(request, foo):
    # Replace hyphens with spaces
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})

    except:
        messages.success(request, ("That category doesn't exist"))
        return redirect('home')


def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html',{})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You Have Been Logged In"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error, please try again"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out!"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("User name Created - Please fill out your billing information"))
            return redirect('update_info')
        else:
            messages.success(request, ("There was a problem Registering, please try again"))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})