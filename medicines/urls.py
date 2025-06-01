from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('medicine/<int:pk>/', views.MedicineDetailView.as_view(), name='medicine-detail'),
    path('medicine/new/', views.MedicineCreateView.as_view(), name='medicine-create'),
    path('medicine/<int:pk>/update/', views.MedicineUpdateView.as_view(), name='medicine-update'),
    path('medicine/<int:pk>/delete/', views.MedicineDeleteView.as_view(), name='medicine-delete'),

    path('export-csv/', views.export_medicines_csv, name='export-csv'),
]