from django.db import models
from django.contrib.auth.models import User
from groups.models import Group


class Expense(models.Model):
    added_by = models.ForeignKey(to=User,on_delete=models.SET(-1), related_name='expense_by_me')
    group = models.ForeignKey(to=Group, on_delete=models.SET(-1), related_name='expenses')
    desc = models.CharField(max_length=150)
    amount = models.FloatField()

    def __str__(self):
        return self.desc


class Borrow(models.Model):
    desc = models.CharField(max_length=150)
    giver = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='borrowed_by')
    taker = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='borrowed_from')
    amount = models.FloatField()
    is_returned = models.BooleanField(default=False)
    date_given = models.DateField(default='1900-01-01')
    entry_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "To {0} for {1} by {2}".format(self.taker.first_name, self.desc, self.giver.first_name)


class Payment(models.Model):
    money = models.FloatField()
    received_by = models.ForeignKey(to=User, on_delete=models.SET(-1), related_name='paid_by')
    returned_by = models.ForeignKey(to=User, on_delete=models.SET(-1), related_name='paid_to')
    created_date = models.DateTimeField(auto_now_add=True)


class Passbook(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='transactions')
    expense = models.ForeignKey(to=Expense, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.expense.desc