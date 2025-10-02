from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

# Home Page View
def home(request):
    """
    Home page view - Shows landing page for non-authenticated users
    """
    return render(request, 'core/home.html')

# Dashboard View
@login_required
def dashboard(request):
    """
    Dashboard view - Shows dashboard for authenticated users
    Retrieves real invoice statistics from the invoices app
    """
    # Import here to avoid circular imports
    from django.db.models import Sum, Count
    from invoices.models import Invoice
    
    # Get user's invoices
    invoices = Invoice.objects.filter(user=request.user)
    
    # Calculate stats
    context = {
        'total_invoices': invoices.count(),
        'paid_invoices': invoices.filter(status='paid').count(),
        'unpaid_invoices': invoices.exclude(status='paid').count(),
        'total_revenue': invoices.filter(status='paid').aggregate(Sum('total'))['total__sum'] or 0,
    }
    
    return render(request, 'core/dashboard.html', context)

