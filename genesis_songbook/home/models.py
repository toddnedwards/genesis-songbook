from django.db import models
from django.utils import timezone

class Show(models.Model):
    date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    location = models.CharField(max_length=200, help_text="City, Country or State")
    ticket_link = models.URLField(blank=True, null=True, help_text="Link to buy tickets")
    description = models.TextField(blank=True, null=True, help_text="Additional show information")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date']
    
    def __str__(self):
        return f"{self.date.strftime('%B %d, %Y')} - {self.venue}"
    
    @property
    def is_past(self):
        """Check if show date has passed"""
        return self.date < timezone.now()
    
    @classmethod
    def upcoming_shows(cls):
        """Get all upcoming shows"""
        return cls.objects.filter(date__gte=timezone.now()).order_by('date')
