from django.urls import path
from . import views
urlpatterns = [
   path('', views.BASE.as_view(), name='home'),
]