from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Q
import csv
import datetime

from .models import Medicine
from .forms import MedicineForm, MedicineSearchForm


class DashboardView(LoginRequiredMixin, ListView):
    model = Medicine
    template_name = 'medicines/dashboard.html'
    context_object_name = 'medicines'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Medicine.objects.all()
        
        # Filter by user if not admin
        if not self.request.user.profile.role == 'admin':
            queryset = queryset.filter(added_by=self.request.user)
        
        # Apply search filters if provided
        form = MedicineSearchForm(self.request.GET)
        if form.is_valid():
            search_query = form.cleaned_data.get('search_query')

            expiry_status = form.cleaned_data.get('expiry_status')
            
            if search_query:
                queryset = queryset.filter(
                    Q(name__icontains=search_query) | 
                    Q(batch_number__icontains=search_query) | 
                    Q(description__icontains=search_query)
                )
            

            
            if expiry_status:
                today = timezone.now().date()
                if expiry_status == 'expired':
                    queryset = queryset.filter(expiry_date__lt=today)
                elif expiry_status == 'expiring_soon':
                    queryset = queryset.filter(expiry_date__gte=today, expiry_date__lte=today + datetime.timedelta(days=7))
                elif expiry_status == 'near_expiry':
                    queryset = queryset.filter(expiry_date__gte=today, expiry_date__lte=today + datetime.timedelta(days=30))
                elif expiry_status == 'safe':
                    queryset = queryset.filter(expiry_date__gt=today + datetime.timedelta(days=30))
        
        return queryset.order_by('expiry_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = MedicineSearchForm(self.request.GET)
        
        # Add expiry statistics
        today = timezone.now().date()
        context['expired_count'] = Medicine.objects.filter(expiry_date__lt=today).count()
        context['expiring_soon_count'] = Medicine.objects.filter(
            expiry_date__gte=today, 
            expiry_date__lte=today + datetime.timedelta(days=7)
        ).count()
        context['near_expiry_count'] = Medicine.objects.filter(
            expiry_date__gt=today + datetime.timedelta(days=7), 
            expiry_date__lte=today + datetime.timedelta(days=30)
        ).count()
        
        return context


class MedicineDetailView(LoginRequiredMixin, DetailView):
    model = Medicine
    template_name = 'medicines/medicine_detail.html'
    context_object_name = 'medicine'


class MedicineCreateView(LoginRequiredMixin, CreateView):
    model = Medicine
    form_class = MedicineForm
    template_name = 'medicines/medicine_form.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        form.instance.added_by = self.request.user
        messages.success(self.request, f'Medicine {form.instance.name} has been added!')
        return super().form_valid(form)


class MedicineUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Medicine
    form_class = MedicineForm
    template_name = 'medicines/medicine_form.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, f'Medicine {form.instance.name} has been updated!')
        return super().form_valid(form)
    
    def test_func(self):
        medicine = self.get_object()
        return self.request.user.profile.role == 'admin' or medicine.added_by == self.request.user


class MedicineDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Medicine
    template_name = 'medicines/medicine_confirm_delete.html'
    success_url = reverse_lazy('dashboard')
    context_object_name = 'medicine'
    
    def delete(self, request, *args, **kwargs):
        medicine = self.get_object()
        messages.success(request, f'Medicine {medicine.name} has been deleted!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        medicine = self.get_object()
        return self.request.user.profile.role == 'admin' or medicine.added_by == self.request.user





@login_required
def export_medicines_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="medicines.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Batch Number', 'Expiry Date', 'Quantity', 
                    'Storage Location', 'Storage Condition', 'Days Until Expiry', 'Status'])
    
    # Get filtered queryset if filters are applied
    form = MedicineSearchForm(request.GET)
    if form.is_valid():
        queryset = DashboardView(request=request).get_queryset()
    else:
        queryset = Medicine.objects.all()
        
        # Filter by user if not admin
        if not request.user.profile.role == 'admin':
            queryset = queryset.filter(added_by=request.user)
    
    for medicine in queryset:
        writer.writerow([
            medicine.name,
            medicine.batch_number,
            medicine.expiry_date,
            medicine.quantity,
            medicine.storage_location or 'N/A',
            medicine.get_storage_condition_display(),
            medicine.days_until_expiry(),
            medicine.expiry_status()
        ])
    
    return response
