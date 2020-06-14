from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_listings, name='display_listing')
]
