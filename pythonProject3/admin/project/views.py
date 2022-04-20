import datetime
from django.shortcuts import render, redirect
from .forms import RegisterForm, ProductForm, ProductPhotoForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Photo, Product, Cart, Wish, Orders, OrderDatails
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.http import JsonResponse
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY  # new


def index(request):
    return render ( request, "index.html" )


def mylogin(request):
    if request.method == "POST":
        user = authenticate ( request, username=request.POST.get ( "username" ),
                              password=request.POST.get ( "password" ) )
        if user is not None:
            login ( request, user )
            return redirect ( "myaccount" )
    return render ( request, "login.html" )


@login_required ( login_url="mylogin" )
def myaccount(request):
    return render ( request, "myaccount.html", {"user": request.user} )


def log(request):
    logout ( request )
    return redirect ( "mylogin" )


def register(request):
    form = RegisterForm ()
    if request.method == "POST":
        form = RegisterForm ( request.POST )
        print ( form.is_valid () )
        if form.is_valid ():
            form = form.save ( commit=False )
            form.is_active = False
            form.save ()
            current_site = get_current_site ( request )
            mail_subject = 'Activate your blog account.'
            message = render_to_string ( 'acc_active_email.html', {
                'user': form,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode ( force_bytes ( form.pk ) ),
                'token': account_activation_token.make_token ( form ),
            } )
            to_email = form.email
            email = EmailMessage (
                mail_subject, message, to=[to_email]
            )
            print ( email )
            email.send ()
            return redirect ( "mylogin" )
    return render ( request, "register.html", {"form": form} )


def activate(request, uidb64, token):
    try:
        uid = force_str ( urlsafe_base64_decode ( uidb64 ) )
        user = User.objects.get ( pk=uid )
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token ( user, token ):
        user.is_active = True
        user.save ()
        login ( request, user )
        # return redirect('home')
        return redirect ( "mylogin" )
    else:
        return HttpResponse ( 'Activation link is invalid!' )


def cart(request):
    product = Cart.objects.all ().filter ( user_id=request.user.id )
    total = 0
    for i in product:
        total += (i.count * i.product.price)
    data = {
        'product': product,
        'total': total,
        'key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render ( request, 'cart.html', data )


def wishlist(request):
    product = Wish.objects.all ().filter ( user_id=request.user.id )
    return render ( request, 'wishlist.html', {'product': product} )


def myAAccount(request):
    return render ( request, 'myAAccount.html' )


def myProduct(request):
    product = Product.objects.all ().prefetch_related ( 'photo' ).filter ( user_id=request.user.id )
    paginator = Paginator ( product, 8 )
    product = request.GET.get ( 'page' )
    product = paginator.get_page ( product )
    return render ( request, 'myProduct.html', {"product": product} )


def prodDetails(request, id):
    info = Product.objects.prefetch_related ( 'photo' ).get ( pk=id )
    print ( info )
    return render ( request, "prodDetails.html", {'info': info} )


def addProduct(request):
    form = ProductForm ()
    imageform = ProductPhotoForm ()
    if request.method == "POST":
        form = ProductForm ( request.POST )
        imageform = ProductPhotoForm ( request.POST, request.FILES )
        if form.is_valid () and imageform.is_valid ():
            form = form.save ( commit=False )
            form.user_id = request.user.id
            form.save ()
            for i in request.FILES.getlist ( "photo_url" ):
                p = Photo ( photo_url=i, product_id=form.id )
                p.save ()
            return redirect ( "index" )
    return render ( request, "addproduct.html", {"form": form, "imageform": imageform, } )


def index2(request):
    product = Product.objects.all ().prefetch_related ( 'photo' )
    return render ( request, 'index-2.html', {'product': product} )


def deleteProcduct(request, id):
    delete = Product.objects.get ( id=id )
    delete.delete ()
    return redirect ( "myProduct" )


def edit(request, id):
    edit = Product.objects.get ( pk=id )
    if request.method == "POST":
        edit.name = request.POST.get ( "name" )
        edit.price = request.POST.get ( "price" )
        edit.count = request.POST.get ( "count" )
        edit.description = request.POST.get ( "description" )
        edit.save ()
        return redirect ( "myProduct" )
    return render ( request, "edit.html", {"edit": edit} )


def addwish(request):
    print ( 'ok' )
    data = json.loads ( request.body.decode ( "utf-8" ) )
    print ( data )
    wish = Wish (
        product_id=data["id"],
        user_id=request.user.id,
    )
    wish.save ()

    return JsonResponse ( {"status": "ok"} )


def addcart(request):
    data = json.loads ( request.body.decode ( "utf-8" ) )
    print ( data )
    try:
        cart = Cart.objects.get ( product_id=data["id"],
                                  user_id=request.user.id )
        cart.count += 1
        cart.save ()
    except:
        cart = Cart (
            product_id=data["id"],
            user_id=request.user.id,
            count=1
        )
        cart.save ()
    return JsonResponse ( {"statsus": "ok"} )


def shopcolumn(request):
    product = Product.objects.all ().prefetch_related ( 'photo' )
    return render ( request, "shopcolumn.html", {'product': product} )


def deleteCart(request, id):
    db = Cart.objects.get ( product_id=id )
    db.delete ()
    return redirect ( 'myProduct' )


def deleteWish(request, id):
    db = Wish.objects.get ( product_id=id )
    db.delete ()
    return redirect ( 'myProduct' )


@login_required ( login_url="mylogin" )
def charge(request):
    print ( "ok" )
    if request.method == 'POST':
        product = Cart.objects.filter ( user_id=request.user.id )
        total = 0
        for i in product:
            total += (i.count * i.product.price)
        print ( request.POST['stripeToken'] )
        charge = stripe.Charge.create (
            amount=int ( total ) * 100,
            currency='usd',
            description='charge',
            source=request.POST['stripeToken']
        ),
        order = Orders (
            total=float ( total ),
            user_id=request.user.id,
            date=datetime.datetime.now ()

        )
        order.save ()
        for j in product:
            orderDatails = OrderDatails (
                count=j.count,
                feedback='',
                order_id=order.id,
                product_id=j.product.id
            )
            orderDatails.save ()
            j.product.count -= j.count
            j.product.save ()
        db = Cart.objects.get ( user_id=request.user.id )
        db.delete ()
        return redirect ( 'order' )


def feedback(request):
    feedback = json.loads ( request.body.decode ( "utf-8" ) )
    order_feedback = OrderDatails.objects.filter ( product_id=feedback["id"] )
    if request.method == "POST":
        for i in order_feedback:
            i.feedback = feedback["feedback"]
            i.save ()
    return redirect ( 'order' )


def shop(request):
    return render ( request, "shop-4-column.html"  )