from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Wallet, Transaction
from .services import detect_fraud
from django.contrib.auth import login , logout
from django.contrib.auth.forms import UserCreationForm
from .forms import DepositForm, WithdrawalForm, TransferForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(
                request,
                "🎉 Registration successful! You can now log in."
            )
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'wallet_app/register.html', {
        'form': form
    })

@login_required
def deposit_view(request):
    form = DepositForm(request.POST or None)
    if form.is_valid():
        currency = form.cleaned_data['currency']
        amt      = form.cleaned_data['amount']
        desc     = form.cleaned_data['description']
        
        wallet, _ = Wallet.objects.get_or_create(
            user=request.user,
            currency=currency
        )
        with transaction.atomic():
            wallet.balance += amt
            wallet.save()
            tx = Transaction.objects.create(
                wallet=wallet,
                transaction_type=Transaction.DEPOSIT,
                amount=amt,
                description=desc
            )
            detect_fraud(tx)
        messages.success(request, f"{currency} ₹{amt} deposited successfully.")
        return redirect('wallet_app:deposit')

    return render(request, 'wallet_app/deposit.html', {
        'form': form,
        'wallets': request.user.wallets.all()
    })

@login_required
def withdraw_view(request):
    form = WithdrawalForm(request.POST or None)
    if form.is_valid():
        currency = form.cleaned_data['currency']
        amt      = form.cleaned_data['amount']
        desc     = form.cleaned_data['description']
        wallet, _ = Wallet.objects.get_or_create(
            user=request.user, currency=currency
        )
        if wallet.balance < amt:
            form.add_error('amount', 'Insufficient balance')
        else:
            with transaction.atomic():
                wallet.balance -= amt
                wallet.save()
                tx = Transaction.objects.create(
                    wallet=wallet,
                    transaction_type=Transaction.WITHDRAWAL,
                    amount=amt,
                    description=desc
                )
                detect_fraud(tx)
            messages.success(request, f"{currency} ₹{amt} withdrawn successfully.")
            return redirect('wallet_app:withdraw')

    return render(request, 'wallet_app/withdraw.html', {
        'form': form,
        'wallets': request.user.wallets.all()
    })

@login_required
def transfer_view(request):
    form = TransferForm(request.POST or None)
    if form.is_valid():
        currency      = form.cleaned_data['currency']
        recipient_user= form.cleaned_data['recipient']
        amt           = form.cleaned_data['amount']
        desc          = form.cleaned_data['description']

        sender_wallet, _ = Wallet.objects.get_or_create(
            user=request.user, currency=currency
        )
        recipient_wallet, _ = Wallet.objects.get_or_create(
            user=recipient_user, currency=currency
        )

        if sender_wallet == recipient_wallet:
            form.add_error('recipient', 'Cannot transfer to yourself')
        elif sender_wallet.balance < amt:
            form.add_error('amount', 'Insufficient balance')
        else:
            with transaction.atomic():
                sender_wallet.balance -= amt
                sender_wallet.save()
                tx1 = Transaction.objects.create(
                    wallet=sender_wallet,
                    transaction_type=Transaction.TRANSFER,
                    amount=amt,
                    related_wallet=recipient_wallet,
                    description=desc
                )
                detect_fraud(tx1)

                
                recipient_wallet.balance += amt
                recipient_wallet.save()
                tx2 = Transaction.objects.create(
                    wallet=recipient_wallet,
                    transaction_type=Transaction.DEPOSIT,
                    amount=amt,
                    related_wallet=sender_wallet,
                    description=f"From {request.user.username}: {desc}"
                )
                detect_fraud(tx2)

            messages.success(
                request,
                f"{currency} ₹{amt} transferred to {recipient_user.username}."
            )
            return redirect('wallet_app:transfer')

    return render(request, 'wallet_app/transfer.html', {
        'form': form,
        'wallets': request.user.wallets.all()
    })

@login_required
def history_view(request):
    txs = Transaction.all_objects.filter(
        wallet__user=request.user
    ).select_related('wallet__currency','related_wallet').order_by('-timestamp')[:100]
    return render(request, 'wallet_app/history.html', {
        'transactions': txs,
        'wallets': request.user.wallets.all()
    })

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')
