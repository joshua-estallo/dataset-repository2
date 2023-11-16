from django.urls import path
from . import views

urlpatterns = [
  path("", views.home, name="home"),
  path("dataset/<int:pk>/", views.dataset, name="dataset"),
  path('upload/', views.upload, name='upload'),
  path('download/<int:pk>/', views.download, name='download'),
]