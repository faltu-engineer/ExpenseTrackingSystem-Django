from django.urls import path,include
from django.conf.urls import url
from expense.views import home, AddExpenseView,ExpenseView

urlpatterns = [
    path('', home, name='expense_home'),
    path('add/<int:pk>/', AddExpenseView.as_view(), name='add_expense'),
    path('view/<int:pk>/', ExpenseView.as_view() , name='expense_view')
]
