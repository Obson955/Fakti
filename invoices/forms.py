from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.forms import inlineformset_factory

from .models import Client, Invoice, InvoiceItem


class ClientForm(forms.ModelForm):
    """Form for creating and updating clients"""
    
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'address', 'city', 'country', 'notes']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class InvoiceForm(forms.ModelForm):
    """Form for creating and updating invoices"""
    
    issue_date = forms.DateField(
        label=_("Issue Date"),
        initial=timezone.now().date(),
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    due_date = forms.DateField(
        label=_("Due Date"),
        initial=lambda: timezone.now().date() + timezone.timedelta(days=30),
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    class Meta:
        model = Invoice
        fields = [
            'client', 'invoice_number', 'issue_date', 'due_date', 'currency',
            'tax_percent', 'discount_percent', 'notes', 'status'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # If we have a user, filter the client choices to only show this user's clients
        if self.user:
            self.fields['client'].queryset = Client.objects.filter(user=self.user)
            
            # Generate next invoice number
            if not self.instance.pk:  # Only for new invoices
                year = timezone.now().year
                # Count invoices for this user this year and add 1
                count = Invoice.objects.filter(
                    user=self.user, 
                    created_at__year=year
                ).count() + 1
                
                # Format: INV-YYYY-00001
                self.fields['invoice_number'].initial = f"INV-{year}-{count:05d}"


class InvoiceItemForm(forms.ModelForm):
    """Form for invoice items"""
    
    class Meta:
        model = InvoiceItem
        fields = ['description', 'quantity', 'unit_price']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }


# Create a formset for invoice items
InvoiceItemFormSet = inlineformset_factory(
    Invoice,
    InvoiceItem,
    form=InvoiceItemForm,
    extra=1,
    min_num=1,
    validate_min=True,
    can_delete=True
)