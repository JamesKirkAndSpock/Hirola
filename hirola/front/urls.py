from django.urls import path

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
    path('reset_password', views.reset_password_view, name='reset_password'),
    path('new_password', views.new_password_view, name='new_password'),
    path('checkout', views.checkout_view, name='checkout'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('imei', views.imei_view, name='imei')
]
