from django.urls import path
from .views import (
    landing_view,
    RegisterView,  # API View
    register_view,  # Web View
    # KeystrokeSubmitView,
    # UserProfileView
)

urlpatterns = [
    path('', landing_view, name='landing'),
    path('register/', register_view, name='register'),
    path('api/register/', RegisterView.as_view(), name='api-register'),  # Для API запитів
    # path('api/keystrokes/', KeystrokeSubmitView.as_view(), name='keystrokes'),
    # path('api/profile/', UserProfileView.as_view(), name='profile'),
]