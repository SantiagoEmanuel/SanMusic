from django.urls import path
from . import views

urlpatterns = [
    # URLS
    path('', views.index, name='index'),

    # API
    path('api/<int:song_id>', views.song_api, name='song_api'),
    
    # AUTHENTICATION
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
]