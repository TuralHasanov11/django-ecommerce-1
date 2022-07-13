from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views
from .forms import PwdResetConfirmForm, PwdResetForm, UserLoginForm

app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/auth/login.html',
                                                form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name='logout'),
    path('register/', views.register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    # Reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="account/auth/password_reset_form.html",
                                                                 success_url='password_reset_email_confirm',
                                                                 email_template_name='account/auth/password_reset_email.html',
                                                                 form_class=PwdResetForm), name='pwdreset'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='account/auth/password_reset_confirm.html',
                                                                                                success_url='password_reset_complete/',
                                                                                                form_class=PwdResetConfirmForm),
         name="password_reset_confirm"),
    path('password_reset/password_reset_email_confirm/',
         TemplateView.as_view(template_name="account/auth/password_reset_status.html"), name='password_reset_done'),
    path('password_reset_confirm/Mg/password_reset_complete/',
         TemplateView.as_view(template_name="account/auth/password_reset_status.html"), name='password_reset_complete'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit, name='edit'),
    path('profile/delete/', views.delete, name='delete'),
    path('profile/delete_confirm/', TemplateView.as_view(template_name="account/user/delete_confirm.html"), name='delete_confirmation'),
     path("addresses/", views.viewAddress, name="addresses"),
    path("add_address/", views.addAddress, name="add_address"),
    path("addresses/edit/<slug:id>/", views.editAddress, name="edit_address"),
    path("addresses/delete/<slug:id>/", views.deleteAddress, name="delete_address"),
    path("addresses/set_default/<slug:id>/", views.setDefaultAddress, name="set_default_address"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("wishlist/toggle/<int:id>", views.addToWishlist, name="toggle_wishlist"),
]