from django.db import models
from django.conf import settings

class Phase(models.Model):
    name = models.CharField(max_length=255)
    phase_number = models.IntegerField()
    open_phase = models.BooleanField(default=True)
    won = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class TaskType(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)  # Store the icon name or path

    def __str__(self):
        return self.name

class LeadSource(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Opportunity(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='opportunities')
    client = models.ForeignKey('core.Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phase = models.ForeignKey(Phase, on_delete=models.SET_NULL, null=True)
    competition = models.ManyToManyField('core.Company', related_name='competitions')
    client_contacts = models.ManyToManyField('core.Contact', related_name='opportunities')
    problem = models.TextField()
    project = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    priority = models.TextField()
    term = models.TextField()
    decision_process = models.TextField()
    source = models.ForeignKey(LeadSource, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='tasks')
    description = models.TextField()
    due_date = models.DateField()
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True)
    moved_from = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='moved_to')
    outcome = models.TextField()
    moved_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.task_type.name} for {self.opportunity.name}'
