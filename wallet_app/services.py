from datetime import timedelta
from django.utils import timezone
from .models import Transaction, Flag
from django.core.mail import send_mail
from django.conf import settings

# ---- Parameters to tune ----
TRANSFER_RATE_LIMIT  = 5        # max transfers in 1-hour window
WITHDRAWAL_THRESHOLD = 10000    # ₹10,000 is “large”

def detect_fraud(tx: Transaction):
    """
    Inspect a newly created transaction and, if it violates a rule,
    create a Flag linked to that transaction.
    """
    # 1) Too many transfers in the past hour?
    if tx.transaction_type == Transaction.TRANSFER:
        window_start = timezone.now() - timedelta(hours=1)
        recent_count = Transaction.all_objects.filter(
            wallet=tx.wallet,
            transaction_type=Transaction.TRANSFER,
            timestamp__gte=window_start
        ).count()
        if recent_count > TRANSFER_RATE_LIMIT:
            flag, created = Flag.objects.get_or_create(
                transaction=tx,
                defaults={'reason': f'{recent_count} transfers in past hour'}
            )
            if created:
                # Mock email alert
                send_mail(
                    subject="Suspicious Transfers Alert",
                    message=(
                        f"{tx.wallet.user.username} made "
                        f"{recent_count} transfers within one hour "
                        f"(latest at {tx.timestamp})."
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )

    # 2) Single large withdrawal?
    if tx.transaction_type == Transaction.WITHDRAWAL and tx.amount > WITHDRAWAL_THRESHOLD:
        flag, created = Flag.objects.get_or_create(
            transaction=tx,
            defaults={'reason': f'Large withdrawal of ₹{tx.amount}'}
        )
        if created:
            send_mail(
                subject="Large Withdrawal Alert",
                message=(
                    f"{tx.wallet.user.username} withdrew ₹{tx.amount} "
                    f"on {tx.timestamp}."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
