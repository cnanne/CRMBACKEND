from django.db import models
from core.models import Company, Contact

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    providers = models.ManyToManyField(Company, related_name='events', limit_choices_to={'is_provider': True})

    def __str__(self):
        return self.name

class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='event_participations')
    was_invited = models.BooleanField(default=False)
    confirmed_participation = models.BooleanField(default=False)
    participated = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.contact} - {self.event}'
