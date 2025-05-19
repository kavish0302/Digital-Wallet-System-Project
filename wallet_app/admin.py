from django.contrib import admin
from .models import Currency, Wallet, Transaction, Flag

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency', 'balance',
                    'created_at', 'updated_at', 'is_active')
    list_filter  = ('currency', 'is_active')
    search_fields= ('user__username',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display  = ('wallet', 'transaction_type',
                     'amount', 'timestamp', 'related_wallet', 'is_active')
    list_filter   = ('transaction_type', 'timestamp', 'wallet')
    search_fields = ('wallet__user__username', 'description')

@admin.register(Flag)
class FlagAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'reason', 'flagged_at')
    list_filter  = ('flagged_at',)
    search_fields= ('reason',)
