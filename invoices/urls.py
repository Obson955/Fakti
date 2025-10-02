from django.urls import path
from . import views

urlpatterns = [
    # Client URLs
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/add/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/edit/', views.ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),
    
    # Invoice URLs
    path('invoices/', views.InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/add/', views.create_invoice, name='invoice_create'),
    path('invoices/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/<int:pk>/edit/', views.edit_invoice, name='invoice_update'),
    path('invoices/<int:pk>/delete/', views.delete_invoice, name='invoice_delete'),
    path('invoices/<int:pk>/status/<str:status>/', views.change_invoice_status, name='invoice_change_status'),
    path('invoices/<int:pk>/pdf/', views.generate_invoice_pdf, name='invoice_pdf'),
    
    # Dashboard
    path('dashboard/', views.invoice_dashboard, name='invoice_dashboard'),
]