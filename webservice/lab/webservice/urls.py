from webservice import views
from django.urls import path

urlpatterns = [
    path('counter.txt', views.counter, name='counter'),
]
