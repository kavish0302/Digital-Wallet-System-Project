from django.db.models import Count
from rest_framework import generics, permissions
from wallet_app.models import Flag, Wallet, Transaction
from rest_framework.response import Response
from wallet_app.serializers import (
    FlaggedTransactionSerializer,
    BalanceSerializer,
    TopUserSerializer
)


# 1) List all flagged transactions (staff only)
class FlaggedTransactionsAPI(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Flag.objects.select_related('transaction__wallet__user')\
                           .order_by('-flagged_at')
    serializer_class = FlaggedTransactionSerializer

# 2) List all user balances
class BalancesAPI(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Wallet.objects.select_related('user')
    serializer_class = BalanceSerializer

# 3) Top users by balance or by transaction volume
class TopUsersAPI(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = TopUserSerializer

    def get_queryset(self):
        # annotate each wallet with their tx count
        return Wallet.objects.select_related('user')\
            .annotate(tx_count=Count('transactions'))

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        by = request.query_params.get('by', 'balance')
        if by == 'volume':
            qs = qs.order_by('-tx_count')
        else:
            qs = qs.order_by('-balance')
        # return top 10
        qs = qs[:10]
        # data = [
        #     {
        #         'username': w.user.username,
        #         'balance':  w.balance,
        #         'tx_count': w.tx_count
        #     } for w in qs
        # ]
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
        data = [
            {
                'username': w.user.username,
                'balance':  w.balance,
                'tx_count': w.tx_count
            } 
            for w in qs
        ]
        return Response(data)
