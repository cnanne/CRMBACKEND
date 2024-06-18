# crm/views.py

from rest_framework import viewsets
from .models import Phase, Opportunity

from .serializers import PhaseSerializer, ClientSerializer, OpportunitySerializer

class PhaseViewSet(viewsets.ModelViewSet):
    queryset = Phase.objects.all()
    serializer_class = PhaseSerializer



class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer
