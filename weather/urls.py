from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.User_logout, name='logout'),

    # Pagination is done to show the data of 30 cities (10 items on every page)
    path('data/<int:page>', views.sample_api, name='logout'),
]