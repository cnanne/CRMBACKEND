from django.db import models
from crm.models import Opportunity
from core.models import Company, Country

class CostSheet(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='cost_sheets')
    description = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cost_sheets')

    @property
    def total_cost_items(self):
        return sum(item.total_cost for item in self.items.all())

    @property
    def total_price_items(self):
        return sum(item.total for item in self.items.all())

    @property
    def total_trip_costs(self):
        return sum(trip.total_cost for trip in self.trips.all())

    @property
    def total_percentage_expenses(self):
        return sum(expense.calculated_expense for expense in self.percentage_expenses.all())

    @property
    def total_generic_expenses(self):
        return sum(expense.amount for expense in self.generic_expenses.all())

    @property
    def total_other_expenses(self):
        return self.total_percentage_expenses + self.total_generic_expenses

    @property
    def total_price_plus_expenses(self):
        return self.total_price_items + self.total_trip_costs + self.total_other_expenses

    def __str__(self):
        return f'{self.opportunity.name} - {self.description}'

class CostSheetItem(models.Model):
    cost_sheet = models.ForeignKey(CostSheet, on_delete=models.CASCADE, related_name='items')
    provider = models.ForeignKey(Company, on_delete=models.CASCADE, limit_choices_to={'is_provider': True}, null=True, blank=True)
    sku = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    @property
    def total(self):
        return self.cost * self.quantity * (1 - self.discount / 100) / (1 - self.margin / 100)

    @property
    def total_cost(self):
        return self.cost * self.quantity * (1 - self.discount / 100)

    @property
    def unit_cost(self):
        return self.cost * (1 - self.discount / 100)

    @property
    def unit_price(self):
        return self.unit_cost / (1 - self.margin / 100)

    def __str__(self):
        return f'{self.cost_sheet.description} - {self.name}'

class Flight(models.Model):
    origin_country = models.CharField(max_length=255)
    destination_country = models.CharField(max_length=255)
    cost_per_trip = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.origin_country} to {self.destination_country}'

class DailyExpense(models.Model):
    country = models.CharField(max_length=255)
    cost_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.country} - {self.cost_per_day}'

class Trip(models.Model):
    cost_sheet = models.ForeignKey(CostSheet, on_delete=models.CASCADE, related_name='trips')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    daily_expense = models.ForeignKey(DailyExpense, on_delete=models.CASCADE)
    days = models.PositiveIntegerField()

    @property
    def total_cost(self):
        return self.flight.cost_per_trip + (self.daily_expense.cost_per_day * self.days)

    def __str__(self):
        return f'{self.cost_sheet.description} - Trip'

class PercentageExpense(models.Model):
    cost_sheet = models.ForeignKey(CostSheet, on_delete=models.CASCADE, related_name='percentage_expenses')
    name = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    expense_type = models.CharField(max_length=50, choices=[
        ('total_cost_sheet', 'Total Cost Sheet'),
        ('total_price', 'Total Price'),
        ('total_cost', 'Total Cost'),
        ('total_profit', 'Total Profit')
    ])

    @property
    def calculated_expense(self):
        total_cost_sheet = self.cost_sheet.total_cost_items + self.cost_sheet.total_trip_costs
        total_price = self.cost_sheet.total_price_items
        total_cost = total_cost_sheet
        total_profit = total_price - total_cost

        if self.expense_type == 'total_cost_sheet':
            return total_cost_sheet * (self.percentage / 100)
        elif self.expense_type == 'total_price':
            return total_price * (self.percentage / 100)
        elif self.expense_type == 'total_cost':
            return total_cost * (self.percentage / 100)
        elif self.expense_type == 'total_profit':
            return total_profit * (self.percentage / 100)
        return 0

    def __str__(self):
        return f'{self.cost_sheet.description} - {self.name}'

class GenericExpense(models.Model):
    cost_sheet = models.ForeignKey(CostSheet, on_delete=models.CASCADE, related_name='generic_expenses')
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.cost_sheet.description} - {self.name}'
