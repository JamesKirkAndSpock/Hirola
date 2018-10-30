from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'front'
urlpatterns = [
    path('', views.page_view, name='landing_page'),
    path('phone_category/<int:category_id>/', views.phone_category_view,
         name='phone_category'),
    path('profile', views.phone_profile_view, name='profile'),
    path('phone_category/<int:category_id>/<int:size>/',
         views.phone_category_size_view, name='phone_category_size'),
    path('sizes', views.sizes, name='sizes'),
    path('area_codes', views.area_codes, name='area_codes'),
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
]
