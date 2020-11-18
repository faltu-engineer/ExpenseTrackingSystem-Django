from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.defaultfilters import register
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from groups.forms import SignUpForm
from groups.tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login
from django.contrib.auth.models import User
from groups.models import Group, GroupMember
from django.db.models import Sum, Count


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def home(request):
    groups = request.user.member_of_groups.all()
    total = request.user.transactions.all().aggregate(Sum('amount'))
    context = {
        "groups": groups,
        'total_expense': total['amount__sum']
    }
    return render(request, 'groups/home.html', context)


@register.filter
def filter_user(expense, _user):
    return expense.passbook_set.filter(user=_user)


def account_activation_sent(request):
    return render(request,'registration/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'registration/account_activation_invalid.html')


@login_required
def group_view(request, pk):
    current_group = Group.objects.get(pk=pk)
    expenses = current_group.expenses.all()
    total_expense = expenses.aggregate(Sum('amount'))
    context = {
        "total_expense": total_expense['amount__sum'],
        "expenses": expenses,
        "current_group": current_group
    }
    return render(request, 'groups/group.html', context)