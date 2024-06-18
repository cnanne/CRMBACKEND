from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import login_view,MyTokenObtainPairView, MyTokenRefreshView

# Initialize the DefaultRouter for routing viewsets
router = DefaultRouter()
# TODO: Register viewsets with the router when models and views are added
# router.register(r'yourmodel', YourModelViewSet)

# Define the URL patterns for the crm app
urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', login_view, name='login'),
    path('auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
]
