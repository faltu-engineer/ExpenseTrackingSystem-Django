from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, DetailView

from expense.models import Expense,Passbook
from groups.models import Group
# Create your views here.


@login_required
def home(request):
    return HttpResponse("Welcome to Expense Page")


class AddExpenseView(LoginRequiredMixin, CreateView):
    model = Expense
    template_name = 'expense/add_expense.html'
    fields = ["desc", "amount"]

    def post(self, request, *args, **kwargs):
        data = request.POST
        current_group = Group.objects.get(pk=kwargs['pk'])
        exp = Expense.objects.create(group=current_group,added_by=request.user,desc=data['desc'],amount=data['amount'])
        exp.desc = data['desc']
        exp.amount = data['amount']
        exp.save()
        all_members = current_group.members.all()
        member_count = len(all_members)
        amount_per_user = float(exp.amount) / member_count
        for member in all_members:
            if request.user.id == member.group_user.id:
                passbook = Passbook.objects.create(user=member.group_user,expense=exp, amount=-amount_per_user)
            else:
                passbook = Passbook.objects.create(user=member.group_user, expense=exp, amount=amount_per_user)
            passbook.save()
        return HttpResponseRedirect("/groups/{0}/".format(kwargs['pk']))


class ExpenseView(LoginRequiredMixin,DetailView):
    model = Expense
    template_name = 'expense/expense_view.html'