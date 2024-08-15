from django.urls import path
from expenses import views as expenses_views
from . import views

urlpatterns = [
    path('', expenses_views.home, name='home'),  # Главная страница
    path('list/', expenses_views.expense_list, name='expense_list'),
    path('add/', expenses_views.add_expense, name='add_expense'),
    path('edit/<int:pk>/', expenses_views.edit_expense, name='edit_expense'),
    path('delete/<int:pk>/', expenses_views.delete_expense, name='delete_expense'),
    path('joke/', views.joke_view, name='joke'),
]