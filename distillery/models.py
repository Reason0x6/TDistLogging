from django.db import models


class FermentationRecord(models.Model):
    """Record for fermentation stage"""
    description = models.CharField(max_length=255, default="Fermentation", help_text="Description")
    to_field = models.CharField(max_length=100, verbose_name="To", help_text="Destination location", blank=True, null=True)
    volume_in_l = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Volume (L)", help_text="Volume in litres", blank=True, null=True)
    start_date = models.DateField(help_text="Start date", blank=True, null=True)
    sg_start = models.FloatField(verbose_name="SG Start", help_text="Starting specific gravity", blank=True, null=True)
    date = models.DateField(verbose_name="End Date", help_text="End date", blank=True, null=True)
    sg_end = models.FloatField(verbose_name="SG End", help_text="Ending specific gravity", blank=True, null=True)
    abv = models.FloatField(verbose_name="ABV (%)", help_text="Alcohol by volume (percent)", blank=True, null=True)
    lal = models.FloatField(verbose_name="LAL", help_text="Litres of Absolute Alcohol", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Fermentation Record"
        verbose_name_plural = "Fermentation Records"
    
    def __str__(self):
        return f"Fermentation ({self.date})"


class DistillationRecord(models.Model):
    """Record for wash/spirit distillation runs"""
    description = models.CharField(max_length=255, help_text="Description of the run")
    faints_in_l = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Faints in (L)", help_text="Faints input in litres", blank=True, null=True)
    from_field = models.CharField(max_length=100, verbose_name="From", help_text="Source location", blank=True, null=True)
    to_field = models.CharField(max_length=100, verbose_name="To", help_text="Destination location", blank=True, null=True)
    volume_in_l = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Volume (L)", help_text="Volume in litres", blank=True, null=True)
    start_date = models.DateField(help_text="Start date", blank=True, null=True)
    date = models.DateField(verbose_name="End Date", help_text="End date", blank=True, null=True)
    abv_harts = models.FloatField(verbose_name="ABV (Harts) %", help_text="ABV of hearts cut", blank=True, null=True)
    lal = models.FloatField(verbose_name="LAL", help_text="Litres of Absolute Alcohol", blank=True, null=True)
    fores_out = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fores out (L)", help_text="Foreshots output", blank=True, null=True)
    heads_out = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Heads out (L)", help_text="Heads output", blank=True, null=True)
    harts_out = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Harts out (L)", help_text="Hearts output", blank=True, null=True)
    tails_out = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tails out (L)", help_text="Tails output", blank=True, null=True)
    waste_out = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Waste out (L)", help_text="Waste output", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Distillation Record"
        verbose_name_plural = "Distillation Records"
    
    def __str__(self):
        return f"{self.description} ({self.date})"


class TotalsRecord(models.Model):
    """Record for batch totals"""
    description = models.CharField(max_length=255, default="Totals", help_text="Description")
    faints_to_storage_l = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Faints to Storage (L)", help_text="Faints stored in litres", blank=True, null=True)
    faints_abv = models.FloatField(verbose_name="Faints ABV (%)", help_text="ABV of stored faints", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Totals Record"
        verbose_name_plural = "Totals Records"
    
    def __str__(self):
        return f"Totals ({self.created_at.date()})"


class ProductRecord(models.Model):
    """Product record linked to a totals record"""
    totals_record = models.ForeignKey(TotalsRecord, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=50, verbose_name="Product", help_text="Product identifier (A, B, C, etc.)")
    final_abv = models.FloatField(verbose_name="Final ABV (%)", help_text="Final alcohol by volume", blank=True, null=True)
    final_l = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Final L", help_text="Final litres", blank=True, null=True)
    distillation_location = models.CharField(max_length=100, verbose_name="Distillation Location", help_text="Location of distillation", blank=True, null=True)
    lal = models.FloatField(verbose_name="LAL", help_text="Litres of Absolute Alcohol", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['product_name']
        verbose_name = "Product Record"
        verbose_name_plural = "Product Records"
    
    def __str__(self):
        return f"Product {self.product_name}"


class Batch(models.Model):
    """A batch with a sequential number and recipe"""
    id = models.AutoField(primary_key=True)
    batch_number = models.IntegerField(unique=True, verbose_name="Batch Number", help_text="Batch number")
    recipe = models.CharField(max_length=255, verbose_name="Recipe", help_text="Recipe name")
    
    # 1:1 Relationships to records
    fermentation = models.OneToOneField(FermentationRecord, on_delete=models.SET_NULL, null=True, blank=True, related_name='batch')
    wash = models.OneToOneField(DistillationRecord, on_delete=models.SET_NULL, null=True, blank=True, related_name='batch_wash')
    spirit_1 = models.OneToOneField(DistillationRecord, on_delete=models.SET_NULL, null=True, blank=True, related_name='batch_spirit1')
    spirit_2 = models.OneToOneField(DistillationRecord, on_delete=models.SET_NULL, null=True, blank=True, related_name='batch_spirit2')
    totals = models.OneToOneField(TotalsRecord, on_delete=models.SET_NULL, null=True, blank=True, related_name='batch')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['batch_number']
        verbose_name = "Batch"
        verbose_name_plural = "Batches"
    
    def __str__(self):
        return f"Batch #{self.batch_number}"
