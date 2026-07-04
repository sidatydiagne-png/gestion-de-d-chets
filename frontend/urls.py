from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('inscription/', views.RegisterPageView.as_view(), name='register'),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('carte/', views.CarteView.as_view(), name='carte'),
    path('signalements/', views.SignalementsListView.as_view(), name='signalements_list'),
    path('signalements/nouveau/', views.SignalementCreateView.as_view(), name='signalement_create'),
    path('zones/', views.ZonesView.as_view(), name='zones'),
    path('collectes/', views.CollectesView.as_view(), name='collectes'),
]