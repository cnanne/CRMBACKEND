# Generated by Django 5.0.1 on 2024-06-18 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_name_role_common_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='role',
        ),
        migrations.AddField(
            model_name='customuser',
            name='roles',
            field=models.ManyToManyField(blank=True, related_name='users', to='accounts.role'),
        ),
        migrations.AddField(
            model_name='role',
            name='groups',
            field=models.ManyToManyField(blank=True, to='auth.group'),
        ),
        migrations.AlterField(
            model_name='role',
            name='key',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
