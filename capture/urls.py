from django.urls import path
from . import views
urlpatterns = [
    path('',views.home),
    path('match/',views.match),
    path('new/',views.new),
]