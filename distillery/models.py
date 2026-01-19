from django.db import models


class Batch(models.Model):
    """A batch with a sequential number and recipe"""
    id = models.AutoField(primary_key=True)
    batch_number = models.IntegerField(unique=True, verbose_name="Batch Number", help_text="Batch number")
    recipe = models.CharField(max_length=255, verbose_name="Recipe", help_text="Recipe name")
    records_data = models.JSONField(default=dict, verbose_name="Records Data", help_text="Dictionary of records for each stage")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['batch_number']
        verbose_name = "Batch"
        verbose_name_plural = "Batches"
    
    def __str__(self):
        return f"Batch #{self.batch_number}"
    
    def get_default_structure(self):
        """Returns the default records structure for a batch"""
        return {
            "Fermentor": [
                {"description": "Fermentor", "record_id": None}
            ],
            "Wash": [
                {"description": "Faints in", "record_id": None},
                {"description": "Still in", "record_id": None},
                {"description": "Fores out", "record_id": None},
                {"description": "Heads out", "record_id": None},
                {"description": "Harts out", "record_id": None},
                {"description": "Tails out", "record_id": None},
                {"description": "Low Wines out", "record_id": None},
                {"description": "Waste out", "record_id": None}
            ],
            "Spirit 1": [
                {"description": "Still in", "record_id": None},
                {"description": "Water In", "record_id": None},
                {"description": "Fores out", "record_id": None},
                {"description": "Heads out", "record_id": None},
                {"description": "Harts out", "record_id": None},
                {"description": "Tails out", "record_id": None},
                {"description": "High Wines out", "record_id": None},
                {"description": "Waste out", "record_id": None},
                {"description": "Filter", "record_id": None},
                {"description": "Low profe Nutral", "record_id": None}
            ],
            "Spirit 2": [
                {"description": "Still in", "record_id": None},
                {"description": "Water In", "record_id": None},
                {"description": "Fores out", "record_id": None},
                {"description": "Heads out", "record_id": None},
                {"description": "Harts out", "record_id": None},
                {"description": "Tails out", "record_id": None},
                {"description": "High Wines out", "record_id": None},
                {"description": "Waste out", "record_id": None},
                {"description": "Filter", "record_id": None},
                {"description": "Low profe Nutral", "record_id": None}
            ],
            "totals": [
                {"description": "High Proof Product Bulk Storage", "record_id": None},
                {"description": "Total Faints Storage", "record_id": None},
                {"description": "Water In", "record_id": None},
                {"description": "Total Low Proof Product A", "record_id": None},
                {"description": "Total Low Proof Product B", "record_id": None},
                {"description": "Carbon Filter", "record_id": None},
                {"description": "Low Proof Product Bulk Store", "record_id": None},
                {"description": "Waste/loss", "record_id": None},
                {"description": "Faints Destroyed", "record_id": None}
            ]
        }
    
    def save(self, *args, **kwargs):
        """Initialize records_data with default structure if empty"""
        if not self.records_data:
            self.records_data = self.get_default_structure()
        super().save(*args, **kwargs)


class Record(models.Model):
    """A record representing a row in the logging table"""
    description = models.CharField(max_length=255, help_text="Description of the record")
    from_field = models.CharField(max_length=100, verbose_name="From", help_text="Source location", blank=True, null=True)
    to_field = models.CharField(max_length=100, verbose_name="To", help_text="Destination location", blank=True, null=True)
    volume_in_l = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Volume in L", help_text="Volume in litres", blank=True, null=True)
    start_date = models.DateField(help_text="Start date", blank=True, null=True)
    sg_start = models.FloatField(verbose_name="SG Start", help_text="Starting specific gravity", blank=True, null=True)
    date = models.DateField(help_text="End date", blank=True, null=True)
    sg_end = models.FloatField(verbose_name="SG End", help_text="Ending specific gravity", blank=True, null=True)
    abv = models.FloatField(verbose_name="ABV", help_text="Alcohol by volume (percent)", blank=True, null=True)
    lal = models.FloatField(verbose_name="LAL", help_text="Litres of Absolute Alcohol", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Record"
        verbose_name_plural = "Records"
    
    def __str__(self):
        return f"{self.description} ({self.date})"
