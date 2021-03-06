from django.urls import path
from django.conf.urls import url

from front import views
from django.contrib.auth.views import (
     PasswordResetDoneView, PasswordResetCompleteView
)

app_name = 'front'
urlpatterns = [
    path('', views.page_view, name='landing_page'),
    path('phone_category/<int:category_id>/', views.phone_category_view,
         name='phone_category'),
    path('profile/<int:phone_model_id>/', views.phone_profile_view,
         name='profile'),
    path('sizes', views.sizes, name='sizes'),
    path('country_codes', views.country_codes, name='country_codes'),
    path('about', views.about_view, name='about'),
    path('signup', views.signup_view, name='signup'),
    path('login', views.login_view, name='login'),
    path('checkout', views.checkout_view, name='checkout'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('imei', views.imei_view, name='imei'),
    path('reset_password', views.PasswordResetViewTailored.as_view(),
         name='password_reset'),
    path('reset_password_done', PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.PasswordResetConfirmViewTailored.as_view(),
        name='password_reset_confirm'
        ),
    path('reset_password/done/', PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path(
        'change_password', views.change_password_view, name='password_change'
    ),
    path('old_password', views.old_password_view, name='password_change_old'),
    path('news', views.press_view, name='news'),
    path('help', views.help_view, name='help'),
    path('teke_vs_others', views.teke_vs_others_view, name='teke_vs_others'),
    path('error', views.error_view, name='error'),
    path('review', views.review_view, name='review'),
    path('review_submit', views.review_submit_view, name='review_submit'),
    path('privacy', views.privacy_view, name='privacy'),
    url(
        r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'
    ),
    path('confirm_user', views.confirm_user_view, name='confirm_user'),
    path('change_email', views.change_email_view, name='change_email'),
    url(
        r'^activate_new_email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_new_email, name='activate_new_email'
    ),
    path('search', views.search_view, name='search'),
    path('change_activation_email/<str:old_email>/',
         views.change_activation_email,
         name='change_activation_email'),
    path('send_link_to_new_address/<str:old_email>/',
         views.send_link_to_new_address,
         name='send_link_to_new_address'),
    path('resend_activation_link/<str:email>/', views.resend_activation_link,
         name='resend_activation_link'),
    path('logout', views.logout_view,
         name='logout'),
    path('resend_new_email_activation_link/',
         views.resend_new_email_activation_link,
         name='resend_new_email_activation_link'),
    path('contact_us', views.contact_us_view, name='contact_us'),
    path('repair_and_network', views.repair_and_network_view,
         name='repair_and_network'),
    path('get_sizes', views.get_sizes, name='get_sizes'),
    path('size_change', views.size_change, name='size_change'),
    path('quantity_change', views.quantity_change, name='quantity_change'),
    path('hot_deal/<int:hot_deal_id>/', views.hot_deal, name='hot_deal'),
    path('hot_deal_quantity_change', views.hot_deal_quantity_change,
         name='hot_deal_quantity_change'),
    path('before_checkout_anonymous', views.before_checkout_anonymous,
         name='before_checkout_anonymous'),
    path('before_checkout', views.before_checkout,
         name='before_checkout'),
    path('order', views.place_order, name='order'),
    path('checkout_complete', views.checkout_complete,
         name='checkout_complete'),
    path('cancel/<int:pk>', views.cancel_order, name='cancel'),
    path('submit_reason', views.submit_reason, name='submit_reason'),
    path('disable_cancel_order', views.disable_cancel_order,
         name='disable_cancel_order'),
    path('confirm/<int:pk>', views.confirm_order_cancellation, name='confirm')
]
