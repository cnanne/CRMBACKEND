# create_roles.py
from accounts.models import Role

roles = [
    {'key': 'account_executive', 'common_name': 'Account Executive'},
    {'key': 'sales_manager', 'common_name': 'Sales Manager'},
    {'key': 'architect', 'common_name': 'Architect'},
    {'key': 'architect_manager', 'common_name': 'Architect Manager'},
    {'key': 'production_manager', 'common_name': 'Production Manager'},
]

for role in roles:
    Role.objects.get_or_create(key=role['key'], defaults={'common_name': role['common_name']})

print("Roles have been created.")
