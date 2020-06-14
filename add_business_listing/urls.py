from django.urls import path
from . import views


urlpatterns = [
    path('', views.add_business, name='add_business'),
]
