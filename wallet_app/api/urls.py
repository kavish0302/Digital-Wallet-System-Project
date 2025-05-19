from django.urls import path
from .views import FlaggedTransactionsAPI, BalancesAPI, TopUsersAPI

app_name = 'wallet_app_api'
urlpatterns = [
    path('flags/',    FlaggedTransactionsAPI.as_view(), name='flags'),
    path('balances/', BalancesAPI.as_view(),          name='balances'),
    path('top-users/',TopUsersAPI.as_view(),          name='top_users'),
]
