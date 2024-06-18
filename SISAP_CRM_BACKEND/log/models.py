from django.db import models
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
import json

class VersionLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=10, choices=[('create', 'Create'), ('update', 'Update'), ('delete', 'Delete')])
    model_name = models.CharField(max_length=255)
    instance_id = models.PositiveIntegerField()
    data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.model_name} - {self.action} - {self.timestamp}'

# Signals to create log entries
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from core.models import Company, Contact, Phone
from events.models import Event, EventParticipant
from crm.models import LeadSource, Opportunity, Phase, Task, TaskType
from costing.models import CostSheet, CostSheetItem, Trip, Flight, DailyExpense, PercentageExpense, GenericExpense

@receiver(pre_save, sender=Company)
@receiver(pre_save, sender=Contact)
@receiver(pre_save, sender=Phone)
@receiver(pre_save, sender=Phase)
@receiver(pre_save, sender=Event)
@receiver(pre_save, sender=EventParticipant)
@receiver(pre_save, sender=LeadSource)
@receiver(pre_save, sender=Opportunity)
@receiver(pre_save, sender=CostSheet)
@receiver(pre_save, sender=Flight)
@receiver(pre_save, sender=DailyExpense)
@receiver(pre_save, sender=Trip)
@receiver(pre_save, sender=CostSheetItem)
@receiver(pre_save, sender=PercentageExpense)
@receiver(pre_save, sender=GenericExpense)
@receiver(pre_save, sender=TaskType)
@receiver(pre_save, sender=Task)
def create_version_log(sender, instance, **kwargs):
    if instance.pk:
        # Update action
        old_instance = sender.objects.get(pk=instance.pk)
        changes = {
            'before': json.dumps(old_instance.__dict__, cls=DjangoJSONEncoder),
            'after': json.dumps(instance.__dict__, cls=DjangoJSONEncoder)
        }
        action = 'update'
    else:
        # Create action
        changes = json.dumps(instance.__dict__, cls=DjangoJSONEncoder)
        action = 'create'
    
    VersionLog.objects.create(
        user=getattr(instance, 'updated_by', None),
        action=action,
        model_name=sender.__name__,
        instance_id=instance.pk,
        data=changes
    )

@receiver(post_delete, sender=Company)
@receiver(post_delete, sender=Contact)
@receiver(post_delete, sender=Phone)
@receiver(post_delete, sender=Phase)
@receiver(post_delete, sender=Event)
@receiver(post_delete, sender=EventParticipant)
@receiver(post_delete, sender=LeadSource)
@receiver(post_delete, sender=Opportunity)
@receiver(post_delete, sender=CostSheet)
@receiver(post_delete, sender=Flight)
@receiver(post_delete, sender=DailyExpense)
@receiver(post_delete, sender=Trip)
@receiver(post_delete, sender=CostSheetItem)
@receiver(post_delete, sender=PercentageExpense)
@receiver(post_delete, sender=GenericExpense)
@receiver(post_delete, sender=TaskType)
@receiver(post_delete, sender=Task)
def log_deletion(sender, instance, **kwargs):
    changes = json.dumps(instance.__dict__, cls=DjangoJSONEncoder)
    VersionLog.objects.create(
        user=getattr(instance, 'updated_by', None),
        action='delete',
        model_name=sender.__name__,
        instance_id=instance.pk,
        data=changes
    )
