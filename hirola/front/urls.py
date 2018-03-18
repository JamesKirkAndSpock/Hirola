from django.urls import path

from . import views

app_name = 'front'
urlpatterns = [
    path('', views.page_view, name='landing_page'),
    path('phone_category', views.phone_category_view, name='phone_category'),
    path('phone', views.phone_view, name='phone'),
]