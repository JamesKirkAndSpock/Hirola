from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'front'
urlpatterns = [
    path('', views.page_view, name='landing_page'),
    path('phone_category/<int:category_id>/', views.phone_category_view,
         name='phone_category'),
    path('profile', views.phone_profile_view, name='profile'),
    path('phone', views.phone_view, name='phone'),
    path('phone_category/<int:category_id>/<int:size>/',
         views.phone_category_size_view, name='phone_category_size'),
    path('sizes', views.sizes, name='sizes'),
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
]
