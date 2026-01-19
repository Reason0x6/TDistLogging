from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from distillery.forms import RecordForm
from distillery.models import Record, Batch
from django.db.models import Q
from datetime import date

def index(request):
    """Home page view showing batches with search functionality."""
    query = request.GET.get('q', '')
    
    # Start with all batches
    batches = Batch.objects.all()
    
    # Apply search filter if query exists
    if query:
        batches = batches.filter(
            Q(recipe__icontains=query) |
            Q(batch_number__icontains=query)
        )
    
    # Order by batch_number descending
    batches = batches.order_by('-batch_number')
    
    # If no search, limit to last 5 batches
    if not query:
        batches = batches[:5]
    
    return render(request, 'index.html', {
        'batches': batches,
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

def log(request, batch_id):
    """Log page view for editing batch records."""
    batch = get_object_or_404(Batch, pk=batch_id)
    
    if request.method == 'POST':
        # Handle form submission for updating records
        # Update records_data based on POST data
        for key in batch.records_data.keys():
            for idx, record_entry in enumerate(batch.records_data[key]):
                record_id = request.POST.get(f'{key}_{idx}_record_id')
                if record_id:
                    batch.records_data[key][idx]['record_id'] = int(record_id) if record_id.isdigit() else None
        
        batch.save()
        messages.success(request, 'Batch records updated successfully!')
        return redirect('log', batch_id=batch.id)
    
    # Get actual Record objects for each entry
    records_with_data = {}
    for key, entries in batch.records_data.items():
        records_with_data[key] = []
        for idx, entry in enumerate(entries):
            record = None
            if entry.get('record_id'):
                try:
                    record = Record.objects.get(pk=entry['record_id'])
                except Record.DoesNotExist:
                    pass
            records_with_data[key].append({
                'description': entry['description'],
                'record_id': entry.get('record_id'),
                'record': record,
                'section': key,
                'index': idx
            })
    
    return render(request, 'log.html', {
        'batch': batch,
        'records_data': records_with_data
    })

def create_batch(request):
    """Create a new batch."""
    if request.method == 'POST':
        batch_number = request.POST.get('batch_number', '')
        recipe = request.POST.get('recipe', '')
        
        # Validate batch number
        try:
            batch_number = int(batch_number)
        except (ValueError, TypeError):
            messages.error(request, 'Batch number must be a valid number.')
            return render(request, 'create_batch.html', {
                'batch_number': batch_number,
                'recipe': recipe
            })
        
        # Check if batch number already exists
        if Batch.objects.filter(batch_number=batch_number).exists():
            messages.error(request, f'Batch #{batch_number} already exists.')
            return render(request, 'create_batch.html', {
                'batch_number': batch_number,
                'recipe': recipe
            })
        
        batch = Batch(batch_number=batch_number, recipe=recipe)
        batch.save()
        messages.success(request, f'Batch #{batch.batch_number} created successfully!')
        return redirect('log', batch_id=batch.batch_number)
    
    # Suggest next batch number
    last_batch = Batch.objects.order_by('-batch_number').first()
    suggested_number = (last_batch.batch_number + 1) if last_batch else 1
    
    return render(request, 'create_batch.html', {'suggested_number': suggested_number})

def create_record(request, batch_id, section, index):
    """Create a new record and link it to a batch."""
    batch = get_object_or_404(Batch, batch_number=batch_id)
    
    # Get the expected description from batch structure
    expected_description = batch.records_data.get(section, [])[int(index)]['description'] if int(index) < len(batch.records_data.get(section, [])) else ''
    
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            record = form.save()
            # Link record to batch
            batch.records_data[section][int(index)]['record_id'] = record.id
            batch.save()
            messages.success(request, f'Record created and linked to Batch #{batch.batch_number}!')
            return redirect('log', batch_id=batch.batch_number)
    else:
        # Pre-fill description and dates with today
        today = date.today()
        form = RecordForm(initial={
            'description': expected_description,
            'start_date': today,
            'date': today
        })
    
    return render(request, 'record_form.html', {
        'form': form,
        'batch': batch,
        'section': section,
        'expected_description': expected_description,
        'is_edit': False
    })

def edit_record(request, batch_id, record_id):
    """Edit an existing record."""
    batch = get_object_or_404(Batch, batch_number=batch_id)
    record = get_object_or_404(Record, pk=record_id)
    
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated successfully!')
            return redirect('log', batch_id=batch.batch_number)
    else:
        form = RecordForm(instance=record)
    
    return render(request, 'record_form.html', {
        'form': form,
        'batch': batch,
        'record': record,
        'is_edit': True
    })
