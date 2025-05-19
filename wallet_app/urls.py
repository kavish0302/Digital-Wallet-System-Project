from django.urls import path
from . import views

app_name = 'wallet_app'

urlpatterns = [
    #path('',        views.home,     name='home'),
    path('register/', views.register_view, name='register'),
    path('deposit/',  views.deposit_view,  name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('transfer/', views.transfer_view, name='transfer'),
    path('history/',  views.history_view,  name='history'),
]
