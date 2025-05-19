from django.db import models
from django.conf import settings
from django.utils import timezone

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)   
    name = models.CharField(max_length=32)              

    class Meta:
        ordering = ['code']

    def __str__(self):
        return self.code

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class Wallet(models.Model):
    user       = models.ForeignKey(
                     settings.AUTH_USER_MODEL,
                     on_delete=models.CASCADE,
                     related_name='wallets'
                 )
    currency   = models.ForeignKey(
                     Currency,
                     on_delete=models.PROTECT
                 )
    balance    = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active  = models.BooleanField(default=True)

    
    objects    = SoftDeleteManager() 
    all_objects= models.Manager()     

    class Meta:
        unique_together = ('user', 'currency')

    def __str__(self):
        return f"{self.user.username}’s {self.currency} Wallet"

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class Transaction(models.Model):
    DEPOSIT    = 'DP'
    WITHDRAWAL = 'WD'
    TRANSFER   = 'TF'
    TRANSACTION_CHOICES = [
        (DEPOSIT,    'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
        (TRANSFER,   'Transfer'),
    ]

    wallet          = models.ForeignKey(
                          Wallet,
                          on_delete=models.CASCADE,
                          related_name='transactions'
                      )
    transaction_type= models.CharField(max_length=2, choices=TRANSACTION_CHOICES)
    amount          = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp       = models.DateTimeField(default=timezone.now)
    related_wallet  = models.ForeignKey(
                          Wallet,
                          on_delete=models.SET_NULL,
                          null=True,
                          blank=True,
                          related_name='related_transactions'
                      )
    description     = models.CharField(max_length=255, blank=True)
    is_active       = models.BooleanField(default=True)

    objects     = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return (
            f"{self.get_transaction_type_display()} {self.amount} "
            f"{self.currency if hasattr(self, 'currency') else ''} "
            f"by {self.wallet.user.username} on {self.timestamp:%Y-%m-%d %H:%M}"
        )

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class Flag(models.Model):
    transaction = models.OneToOneField(
                      Transaction,
                      on_delete=models.CASCADE,
                      related_name='flag'
                  )
    reason      = models.CharField(max_length=255)
    flagged_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Flag: {self.transaction} – {self.reason}"
