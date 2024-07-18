# app/urls.py

from django.urls import path
from .views import ImageProcessingView

urlpatterns = [
    path('my-endpoint/', ImageProcessingView.as_view(), name='my-endpoint'),
    path('process-image/', ImageProcessingView.as_view(), name='process-image'),
]
