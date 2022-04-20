from . import views
from django.contrib import admin
from .forms import MYPasswordChangeForm
from django.urls import path, include,reverse_lazy
from django.contrib.auth import views as auth_views

from django.contrib.auth.views\
    import PasswordChangeView,\
    PasswordChangeDoneView,\
    PasswordResetView, \
    PasswordResetDoneView,\
    PasswordResetConfirmView,\
    PasswordResetCompleteView



urlpatterns = [
    path ( '', views.index, name='index' ),

    path ( 'charge/', views.charge, name='charge' ),
    # path ( 'order/', views.order, name='order' ),
    # path ( 'orderdatails/', views.orderdatails, name='orderdatails' ),
    path ( 'index-2/', views.index2, name='index2' ),
    path ( 'mylogin/', views.mylogin, name='mylogin' ),
    path ( 'register/', views.register, name='register' ),
    path ( 'mylogout/', views.log, name='mylogout' ),
    path ( "activate/<uidb64>/<token>/", views.activate, name='activate' ),
    path ( "myaccount/", views.myaccount, name='myaccount' ),
    path ( 'cart/', views.cart, name='cart' ),
    path ( 'wishlist/', views.wishlist, name='wishlist' ),
    path ( 'delete1/<int:id>/', views.deleteProcduct, name='delete1' ),
    path ( 'delete2/<int:id>/', views.deleteCart, name='delete2' ),
    path ( 'delete3/<int:id>/', views.deleteWish, name='delete3' ),
    path ( 'edit/<int:id>/', views.edit, name='edit' ),
    path ( 'myProduct/', views.myProduct, name='myProduct' ),
    path ( 'addproduct/', views.addProduct, name='addproduct' ),
    path ( 'prodDetails/<int:id>', views.prodDetails, name='prodDetails' ),
    path ( "prodDetails/mycart", views.addcart, name="mycart" ),
    path ( "prodDetails/wish", views.addwish, name="wish" ),
    path ( 'shopcolumn/', views.shopcolumn, name='shopcolumn' ),
    path ( 'shop-4-column/', views.shop, name='shop-4-column' ),

    #  change password & found password
    path ( 'password_change/done/',
           auth_views.PasswordChangeDoneView.as_view (
               template_name='registration/password_change_done.html' ),
           name='password_change_done' ),

    path ( 'password_change/',
           auth_views.PasswordChangeView.as_view ( template_name='registration/password_change.html' ),
           name='password_change' ),

    path ( 'password_reset/done/',
           auth_views.PasswordResetCompleteView.as_view (
               template_name='registration/password_reset_done.html' ),
           name='password_reset_done' ),

    path ( 'reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view (),
           name='password_reset_confirm' ),

    path ( 'password_reset/', auth_views.PasswordResetView.as_view (), name='password_reset' ),

    path ( 'reset/done/',
           auth_views.PasswordResetCompleteView.as_view (
               template_name='registration/password_reset_complete.html' ),
           name='password_reset_complete' ),


]
