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
    path('signup', views.signup_view, name='signup')
]
