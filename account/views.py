from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)
from store.models import Product
from .forms import RegistrationForm, UserEditForm, UserAddressForm
from .models import Account, Address
from .tokens import account_activation_token
from django.urls import reverse
from django.contrib import messages
from orders.views import userOrders

@require_GET
@login_required
def dashboard(request):
    orders = userOrders(request)
    return render(request,
                  'account/user/dashboard.html',
                  {'section': 'profile', 'orders': orders})

@require_http_methods(["POST", "GET"])
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'account/user/edit.html', {'user_form': user_form})

@require_POST
@login_required
def delete(request):
    user = Account.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')

@require_http_methods(["POST", "GET"])
def register(request):

    if request.user.is_authenticated:
        return redirect('account:dashboard')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            currentSite = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/auth/activation_email.html', {
                'user': user,
                'domain': currentSite.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, "account/auth/register_email_confirm.html")
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/auth/register.html', {'form': registerForm})

@require_GET
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/auth/activation_invalid.html')


@login_required
def viewAddress(request):
    addresses = Address.objects.filter(account=request.user)
    return render(request, "account/user/addresses.html", {"addresses": addresses})


@login_required
@require_http_methods(["GET", "POST"])
def addAddress(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.account = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm()
    return render(request, "account/user/edit_addresses.html", {"form": address_form})

@login_required
@require_http_methods(["GET", "POST"])
def editAddress(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, account=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(pk=id, account=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "account/user/edit_addresses.html", {"form": address_form})

@login_required
def deleteAddress(request, id):
    address = Address.objects.filter(pk=id, account=request.user).delete()
    return redirect("account:addresses")

@login_required
def setDefaultAddress(request, id):
    Address.objects.filter(account=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, account=request.user).update(default=True)
    return redirect("account:addresses")   



@login_required
def wishlist(request):
    products = Product.objects.filter(user_wishlist=request.user)
    return render(request, "account/dashboard/user_wish_list.html", {"wishlist": products})


@login_required
def addToWishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.user_wishlist.filter(id=request.user.id).exists():
        product.user_wishlist.remove(request.user)
        messages.success(request, product.title + " has been removed from your WishList")
    else:
        product.user_wishlist.add(request.user)
        messages.success(request, "Added " + product.title + " to your WishList")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])