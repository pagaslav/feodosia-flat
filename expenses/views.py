from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse
from .models import Expense
from .forms import ExpenseForm
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.models import User
from .utils import get_exchange_rates
from .models import Transfer
import requests



def home(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Перенаправление на страницу входа, если пользователь не аутентифицирован
    return redirect('expense_list')  # Перенаправление на страницу списка расходов, если пользователь аутентифицирован

@login_required
def expense_list(request):
    # Current user's expenses
    user_expenses = Expense.objects.filter(user=request.user)
    
    # Total amount of current user's expenses
    total_user_amount = user_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # All users' expenses
    all_expenses = Expense.objects.all()
    
    # Total amount of all users' expenses
    total_all_amount = all_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Analytics per user
    expenses_per_user = Expense.objects.values('user__username').annotate(total=Sum('amount'))
    
    # Analytics per category
    expenses_per_category = Expense.objects.values('category__name').annotate(total=Sum('amount'))

    # Get all users
    users = User.objects.all()

    # Transfers between sisters
    transfers = Transfer.objects.all()

    total_transfers_amount = transfers.aggregate(Sum('amount'))['amount__sum']

    # Fetch a joke from the API
    response = requests.get('https://official-joke-api.appspot.com/jokes/random')
    joke = response.json() if response.status_code == 200 else {"setup": "No joke available", "punchline": "Please try again later."}
    
    context = {
        'user_expenses': user_expenses,
        'total_user_amount': total_user_amount,
        'all_expenses': all_expenses,
        'total_all_amount': total_all_amount,
        'expenses_per_user': expenses_per_user,
        'expenses_per_category': expenses_per_category,
        'users': users,
        'transfers': transfers,
        'total_transfers_amount': total_transfers_amount,
        'joke': joke,
    }
    
    return render(request, 'expenses/expense_list.html', context)

@login_required
def add_expense(request):
    exchange_rates = get_exchange_rates()
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            if not expense.date:
                expense.date = None  # Установите дату в None, если она не была указана
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm()

     # Добавляем атрибут type="date" к полю date
    form.fields['date'].widget.attrs.update({'type': 'date', 'class': 'form-control'})

    return render(request, 'expenses/add_expense.html', {'form': form, 'exchange_rates': exchange_rates})

@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/edit_expense.html', {'form': form})

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('expense_list')
    
    return render(request, 'expenses/delete_expense.html', {'expense': expense})
    

def joke_view(request):
    response = requests.get('https://official-joke-api.appspot.com/jokes/random')
    joke = response.json()
    
    return render(request, 'joke.html', {'joke': joke})