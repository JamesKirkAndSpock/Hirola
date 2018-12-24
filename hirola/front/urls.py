from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'front'
urlpatterns = [
    path('', views.page_view, name='landing_page'),
    path('phone_category/<int:category_id>/', views.phone_category_view,
         name='phone_category'),
    path('profile/<int:phone_id>/', views.phone_profile_view, name='profile'),
    path('phone_category/<int:category_id>/<int:size>/',
         views.phone_category_size_view, name='phone_category_size'),
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
    path('reset_password_done', views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.PasswordResetConfirmViewTailored.as_view(),
        name='password_reset_confirm'),
    path('reset_password/done/', views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('change_password', views.change_password_view, name='password_change'),
    path('old_password', views.old_password_view, name='password_change_old'),
    path('news', views.press_view, name='news'),
    path('help', views.help_view, name='help'),
    path('teke_vs_others', views.teke_vs_others_view, name='teke_vs_others'),
    path('error', views.error_view, name='error'),
    path('review', views.review_view, name='review'),
    path('review_submit', views.review_submit_view, name='review_submit'),
    path('privacy', views.privacy_view, name='privacy'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('confirm_user', views.confirm_user_view, name='confirm_user'),
    path('change_email', views.change_email_view, name='change_email'),
    url(r'^activate_new_email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_new_email, name='activate_new_email'),
    path('search', views.search_view, name='search')
]
