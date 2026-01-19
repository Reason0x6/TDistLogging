from django.shortcuts import render, redirect
from django.contrib import messages
from distillery.forms import RecordForm
from distillery.models import Record
from django.db.models import Q

def index(request):
    """Home page view."""
    return render(request, 'index.html')

def search(request):
    """Search page view - shows last 15 records from filtered results."""
    query = request.GET.get('q', '')
    
    # Start with all records
    records = Record.objects.all()
    
    # Apply search filter if query exists (searches ALL records)
    if query:
        records = records.filter(
            Q(description__icontains=query) |
            Q(from_field__icontains=query) |
            Q(to_field__icontains=query)
        )
    
    # Order by created_at descending and limit to last 15
    records = records.order_by('-created_at')[:15]
    
    return render(request, 'search.html', {
        'records': records,
        'query': query
    })

def full_log(request):
    """Full log page view - shows all records."""
    query = request.GET.get('q', '')
    
    # Start with all records
    records = Record.objects.all()
    
    # Apply search filter if query exists
    if query:
        records = records.filter(
            Q(description__icontains=query) |
            Q(from_field__icontains=query) |
            Q(to_field__icontains=query)
        )
    
    # Order by created_at descending (no limit)
    records = records.order_by('-created_at')
    
    return render(request, 'full_log.html', {
        'records': records,
        'query': query
    })

def log(request):
    """Log page view."""
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record created successfully!')
            return redirect('log')
    else:
        form = RecordForm()
    
    return render(request, 'log.html', {'form': form})
