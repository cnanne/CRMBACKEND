from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=10)
    sales_tax = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    is_competition = models.BooleanField(default=False)
    is_provider = models.BooleanField(default=False)
    is_enterprise_group = models.BooleanField(default=False)
    parent_group = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subsidiaries')

    def __str__(self):
        return self.name

class Contact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    corporate_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Phone(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='phones')
    phone_number = models.CharField(max_length=20)
    phone_type = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.contact} - {self.phone_number} ({self.phone_type})'
