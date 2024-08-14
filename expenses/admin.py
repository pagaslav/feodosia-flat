from django.contrib import admin
from .models import Category, Expense, Transfer

admin.site.register(Category)
admin.site.register(Expense)

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'amount', 'date')
    list_filter = ('date', 'sender', 'receiver')
    search_fields = ('sender__username', 'receiver__username')
    fields = ('sender', 'receiver', 'amount', 'date') 