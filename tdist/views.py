from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from distillery.forms import FermentationRecordForm, DistillationRecordForm, TotalsRecordForm, ProductRecordForm
from distillery.models import Batch, FermentationRecord, DistillationRecord, TotalsRecord, ProductRecord
from django.db.models import Q
from datetime import date
import csv

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
    """Full log page view - shows all records from all batch types."""
    query = request.GET.get('q', '')
    
    # Gather all records from all types
    fermentation_records = FermentationRecord.objects.all()
    distillation_records = DistillationRecord.objects.all()
    totals_records = TotalsRecord.objects.all()
    
    # Apply search filter if query exists
    if query:
        fermentation_records = fermentation_records.filter(
            Q(description__icontains=query) |
            Q(to_field__icontains=query)
        )
        distillation_records = distillation_records.filter(
            Q(description__icontains=query) |
            Q(from_field__icontains=query) |
            Q(to_field__icontains=query)
        )
        totals_records = totals_records.filter(
            Q(description__icontains=query)
        )
    
    # Combine all records for display
    all_records = []
    
    for record in fermentation_records:
        all_records.append({
            'type': 'Fermentation',
            'record': record,
            'date': record.date
        })
    
    for record in distillation_records:
        all_records.append({
            'type': 'Distillation',
            'record': record,
            'date': record.date
        })
    
    for record in totals_records:
        all_records.append({
            'type': 'Totals',
            'record': record,
            'date': record.created_at.date()
        })
    
    # Sort by date descending
    all_records.sort(key=lambda x: x['date'] if x['date'] else date.min, reverse=True)
    
    return render(request, 'full_log.html', {
        'records': all_records,
        'query': query
    })

def log(request, batch_id):
    """Log page view for editing batch records."""
    batch = get_object_or_404(Batch, batch_number=batch_id)
    
    # Get actual Record objects for each entry
    records_with_data = {}
    for key, entries in batch.records_data.items():
        records_with_data[key] = []
        for idx, entry in enumerate(entries):
            record = None
            record_type = entry.get('record_type', 'legacy')
            
            if entry.get('record_id'):
                try:
                    if record_type == 'fermentation':
                        record = FermentationRecord.objects.get(pk=entry['record_id'])
                    elif record_type == 'distillation':
                        record = DistillationRecord.objects.get(pk=entry['record_id'])
                    elif record_type == 'totals':
                        record = TotalsRecord.objects.get(pk=entry['record_id'])
                    else:
                        record = Record.objects.get(pk=entry['record_id'])
                except (FermentationRecord.DoesNotExist, DistillationRecord.DoesNotExist, 
                        TotalsRecord.DoesNotExist):
                    pass
            
            records_with_data[key].append({
                'description': entry['description'],
                'record_id': entry.get('record_id'),
                'record': record,
                'record_type': record_type,
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
    
    # Get the expected description and record type from batch structure
    entry = batch.records_data.get(section, [])[int(index)] if int(index) < len(batch.records_data.get(section, [])) else {}
    expected_description = entry.get('description', '')
    record_type = entry.get('record_type', 'legacy')
    
    # Determine which form to use based on section/record type
    if record_type == 'fermentation':
        FormClass = FermentationRecordForm
        ModelClass = FermentationRecord
    elif record_type == 'distillation':
        FormClass = DistillationRecordForm
        ModelClass = DistillationRecord
    elif record_type == 'totals':
        FormClass = TotalsRecordForm
        ModelClass = TotalsRecord
    else:
        messages.error(request, 'Unknown record type.')
        return redirect('log', batch_id=batch.batch_number)
    
    if request.method == 'POST':
        form = FormClass(request.POST)
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
        initial_data = {'description': expected_description}
        
        # Add date fields based on record type
        if record_type == 'fermentation':
            initial_data.update({'start_date': today, 'date': today})
        elif record_type == 'distillation':
            initial_data.update({'start_date': today, 'date': today})
        
        form = FormClass(initial=initial_data)
    
    return render(request, 'record_form.html', {
        'form': form,
        'batch': batch,
        'section': section,
        'expected_description': expected_description,
        'record_type': record_type,
        'is_edit': False
    })

def edit_record(request, batch_id, record_id):
    """Edit an existing record."""
    batch = get_object_or_404(Batch, batch_number=batch_id)
    
    # Find the record type from batch records_data
    record_type = 'legacy'
    record = None
    
    for section, entries in batch.records_data.items():
        for entry in entries:
            if entry.get('record_id') == record_id:
                record_type = entry.get('record_type', 'legacy')
                break
        if record_type != 'legacy':
            break
    
    # Get the appropriate form and model
    if record_type == 'fermentation':
        FormClass = FermentationRecordForm
        record = get_object_or_404(FermentationRecord, pk=record_id)
    elif record_type == 'distillation':
        FormClass = DistillationRecordForm
        record = get_object_or_404(DistillationRecord, pk=record_id)
    elif record_type == 'totals':
        FormClass = TotalsRecordForm
        record = get_object_or_404(TotalsRecord, pk=record_id)
    else:
        messages.error(request, 'Unknown record type.')
        return redirect('log', batch_id=batch.batch_number)
    
    if request.method == 'POST':
        form = FormClass(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated successfully!')
            return redirect('log', batch_id=batch.batch_number)
    else:
        form = FormClass(instance=record)
    
    return render(request, 'record_form.html', {
        'form': form,
        'batch': batch,
        'record': record,
        'record_type': record_type,
        'is_edit': True
    })

def export_batch_csv(request, batch_id):
    """Export batch and all its records as CSV."""
    batch = get_object_or_404(Batch, batch_number=batch_id)
    
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="batch_{batch.batch_number}_export.csv"'
    
    writer = csv.writer(response)
    
    # Write batch header info
    writer.writerow(['Batch Information'])
    writer.writerow(['Batch Number', batch.batch_number])
    writer.writerow(['Recipe', batch.recipe])
    writer.writerow(['Created', batch.created_at.strftime('%Y-%m-%d %H:%M')])
    writer.writerow(['Updated', batch.updated_at.strftime('%Y-%m-%d %H:%M')])
    writer.writerow([])  # Empty row for separation
    
    # Write records for each section
    for section, entries in batch.records_data.items():
        writer.writerow([f'=== {section} ==='])
        
        for entry in entries:
            record_id = entry.get('record_id')
            record_type = entry.get('record_type', 'legacy')
            
            if record_id:
                try:
                    if record_type == 'fermentation':
                        record = FermentationRecord.objects.get(pk=record_id)
                        writer.writerow(['Fermentation Record'])
                        writer.writerow(['To', 'Volume (L)', 'Start Date', 'SG Start', 'End Date', 'SG End', 'ABV (%)', 'LAL'])
                        writer.writerow([
                            record.to_field or '',
                            record.volume_in_l or '',
                            record.start_date.strftime('%Y-%m-%d') if record.start_date else '',
                            record.sg_start or '',
                            record.date.strftime('%Y-%m-%d') if record.date else '',
                            record.sg_end or '',
                            record.abv or '',
                            record.lal or ''
                        ])
                    elif record_type == 'distillation':
                        record = DistillationRecord.objects.get(pk=record_id)
                        writer.writerow(['Distillation Record:', record.description])
                        writer.writerow(['Faints In (L)', 'From', 'To', 'Volume (L)', 'Start Date', 'End Date', 'ABV (Harts)', 'LAL', 'Fores Out', 'Heads Out', 'Harts Out', 'Tails Out', 'Waste Out'])
                        writer.writerow([
                            record.faints_in_l or '',
                            record.from_field or '',
                            record.to_field or '',
                            record.volume_in_l or '',
                            record.start_date.strftime('%Y-%m-%d') if record.start_date else '',
                            record.date.strftime('%Y-%m-%d') if record.date else '',
                            record.abv_harts or '',
                            record.lal or '',
                            record.fores_out or '',
                            record.heads_out or '',
                            record.harts_out or '',
                            record.tails_out or '',
                            record.waste_out or ''
                        ])
                    elif record_type == 'totals':
                        record = TotalsRecord.objects.get(pk=record_id)
                        writer.writerow(['Totals Record'])
                        writer.writerow(['Faints to Storage (L)', 'Faints ABV (%)'])
                        writer.writerow([
                            record.faints_to_storage_l or '',
                            record.faints_abv or ''
                        ])
                        
                        # Add products if any
                        products = ProductRecord.objects.filter(totals_record=record)
                        if products.exists():
                            writer.writerow([])
                            writer.writerow(['Products'])
                            writer.writerow(['Product', 'Final ABV (%)', 'Final L', 'Distillation Location', 'LAL'])
                            for product in products:
                                writer.writerow([
                                    product.product_name,
                                    product.final_abv or '',
                                    product.final_l or '',
                                    product.distillation_location or '',
                                    product.lal or ''
                                ])
                except (FermentationRecord.DoesNotExist, DistillationRecord.DoesNotExist, 
                        TotalsRecord.DoesNotExist):
                    writer.writerow([entry['description'], 'Record not found'])
            else:
                writer.writerow([entry['description'], 'No data'])
        
        writer.writerow([])  # Empty row between sections
    
    return response


def add_product(request, batch_id, totals_record_id):
    """Add a product to a totals record."""
    batch = get_object_or_404(Batch, batch_number=batch_id)
    totals_record = get_object_or_404(TotalsRecord, pk=totals_record_id)
    
    if request.method == 'POST':
        form = ProductRecordForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.totals_record = totals_record
            product.save()
            messages.success(request, f'Product {product.product_name} added successfully!')
            return redirect('log', batch_id=batch.batch_number)
    else:
        # Suggest next product letter
        existing_products = ProductRecord.objects.filter(totals_record=totals_record).count()
        suggested_name = chr(65 + existing_products)  # A, B, C, etc.
        form = ProductRecordForm(initial={'product_name': suggested_name})
    
    return render(request, 'product_form.html', {
        'form': form,
        'batch': batch,
        'totals_record': totals_record,
        'is_edit': False
    })


def edit_product(request, batch_id, product_id):
    """Edit a product record."""
    batch = get_object_or_404(Batch, batch_number=batch_id)
    product = get_object_or_404(ProductRecord, pk=product_id)
    
    if request.method == 'POST':
        form = ProductRecordForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product {product.product_name} updated successfully!')
            return redirect('log', batch_id=batch.batch_number)
    else:
        form = ProductRecordForm(instance=product)
    
    return render(request, 'product_form.html', {
        'form': form,
        'batch': batch,
        'product': product,
        'is_edit': True
    })


def delete_product(request, batch_id, product_id):
    """Delete a product record."""
    batch = get_object_or_404(Batch, batch_number=batch_id)
    product = get_object_or_404(ProductRecord, pk=product_id)
    
    if request.method == 'POST':
        product_name = product.product_name
        product.delete()
        messages.success(request, f'Product {product_name} deleted successfully!')
        return redirect('log', batch_id=batch.batch_number)
    
    return render(request, 'confirm_delete_product.html', {
        'batch': batch,
        'product': product
    })
