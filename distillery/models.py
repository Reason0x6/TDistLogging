from django.db import models


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
