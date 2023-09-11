
from django.urls import path
from .views import *

urlpatterns = [
    path('', Index, name="index"),
    path('register/', Register, name="register"),
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    path('uploadexcel/', UploadExcel, name='uploadexcel'),
    path('search/', Search, name='search'),
    path('all_user/', All_user, name='all_user'),
]
