from django.urls import path

from . import views

app_name = 'front'
urlpatterns = [
    path('', views.page_view, name='landing_page'),
    path('phone_category', views.phone_category_view, name='phone_category'),
    path('iphone', views.iphone_view, name='iphone'),
    path('android', views.android_view, name='android'),
    path('tablet', views.tablet_view, name='android'),
    path('profile', views.phone_profile_view, name='profile'),
    path('phone', views.phone_view, name='phone'),
]
