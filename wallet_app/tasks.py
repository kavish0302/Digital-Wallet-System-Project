# from celery import shared_task
# from django.utils import timezone
# from datetime import timedelta
# from .models import Transaction, Flag
# from .services import detect_fraud
# from django.core.mail import send_mail
# from django.conf import settings

# @shared_task
# def daily_fraud_scan():
#     since = timezone.now() - timedelta(days=1)
#     recent_txs = Transaction.objects.filter(timestamp__gte=since)
#     new_flags = []
#     for tx in recent_txs:
#         # detect_fraud will get_or_create Flags
#         before = Flag.objects.filter(transaction=tx).exists()
#         detect_fraud(tx)
#         after = Flag.objects.filter(transaction=tx).exists()
#         if not before and after:
#             new_flags.append(tx)

#     # Send a summary email (mocked)
#     if new_flags:
#         body = "\n".join(
#             f"{tx.wallet.user.username}: {tx.get_transaction_type_display()} ₹{tx.amount} at {tx.timestamp}"
#             for tx in new_flags
#         )
#         send_mail(
#             subject="Daily Fraud Scan Report",
#             message=body,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[settings.DEFAULT_FROM_EMAIL],
#             fail_silently=True,
#         )
#     #return len(new_flags)
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Transaction, Flag
from .services import detect_fraud
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def daily_fraud_scan():
    since = timezone.now() - timedelta(days=1)
    recent_txs = Transaction.all_objects.filter(timestamp__gte=since)
    new_flags = []

    for tx in recent_txs:
        already_flagged = Flag.objects.filter(transaction=tx).exists()
        detect_fraud(tx)
        now_flagged = Flag.objects.filter(transaction=tx).exists()
        if not already_flagged and now_flagged:
            new_flags.append(tx)

    # Email summary if any new flags
    if new_flags:
        lines = [
          f"{tx.wallet.user.username} • {tx.get_transaction_type_display()} ₹{tx.amount} at {tx.timestamp:%Y-%m-%d %H:%M}"
          for tx in new_flags
        ]
        body = "New fraud flags in the last 24 h:\n" + "\n".join(lines)
        send_mail(
          subject="Daily Fraud Scan Report",
          message=body,
          from_email=settings.DEFAULT_FROM_EMAIL,
          recipient_list=[settings.DEFAULT_FROM_EMAIL],
          fail_silently=True,
        )
