from rest_framework import serializers
from .models import Flag, Transaction, Wallet
from django.contrib.auth import get_user_model

User = get_user_model()

class FlaggedTransactionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='transaction.wallet.user.username')
    tx_type  = serializers.CharField(source='transaction.get_transaction_type_display')
    amount   = serializers.DecimalField(source='transaction.amount', max_digits=12, decimal_places=2)
    timestamp= serializers.DateTimeField(source='transaction.timestamp')

    class Meta:
        model = Flag
        fields = ['id', 'username', 'tx_type', 'amount', 'timestamp', 'reason']

class BalanceSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    balance  = serializers.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = Wallet
        fields = ['username', 'balance']

from rest_framework import serializers
from .models import Wallet

class TopUserSerializer(serializers.ModelSerializer):
    # Pull the username from the related User
    username = serializers.CharField(source='user.username')
    # tx_count is an annotation, so DRF will pick it up directly
    tx_count = serializers.IntegerField()

    class Meta:
        model = Wallet
        fields = ['username', 'balance', 'tx_count']

