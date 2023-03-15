from django.contrib import admin
from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('contactus/', views.contactus2, name='contactus'),
    path('contactusclass/', views.ContactUs.as_view(), name='contactclass'),
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('login/', views.LoginViewUser.as_view(), name='login'),
    path('logout/', views.LogoutViewUser.as_view(), name='logout'),
    path('signupseller/', views.RegisterViewSeller.as_view(), name='signupseller'),
    path('testsessions/', views.testsessions, name="testsessions"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    # change password
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='firstapp/registration/password_change_done.html'),
         name='password_change_done'),

    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='firstapp/registration/password_change.html',
                                               success_url=reverse_lazy("password_change_done")),
         name='password_change'),

    # Forgot password
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="firstapp/registration/password_reset_form.html",
                                                     success_url=reverse_lazy("password_reset_complete")),
         name="password_reset_confirm"),  # 3
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="firstapp/registration/password_reset.html",
                                              success_url=reverse_lazy("password_reset_done"),
                                              email_template_name='firstapp/registration/forgot_password_email.html'),
         name="reset_password"),  # 1
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="firstapp/registration/password_reset_sent.html"),
         name="password_reset_done"),  # 2

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="firstapp/registration/password_reset_done.html"),
         name="password_reset_complete"),  # 4

]
