from django.contrib import admin
from django import forms
from .models import Show

class ShowAdminForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = '__all__'
        widgets = {
            'date': forms.SplitDateTimeWidget(
                date_attrs={'type': 'date'},
                time_attrs={'type': 'time', 'step': '1800'}  # 30 minutes
            )
        }

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    form = ShowAdminForm
    list_display = ('date', 'venue', 'location', 'has_ticket_link', 'is_past')
    list_filter = ('date', 'location')
    search_fields = ('venue', 'location', 'description')
    date_hierarchy = 'date'
    ordering = ['-date']
    
    fieldsets = (
        ('Show Information', {
            'fields': ('date', 'venue', 'location'),
            'description': 'Select date and time for the show. Times can be selected in 30-minute intervals.'
        }),
        ('Ticketing', {
            'fields': ('ticket_link',),
            'description': 'Add the URL where people can buy tickets for this show'
        }),
        ('Additional Details', {
            'fields': ('description',),
            'classes': ('collapse',)
        })
    )
    
    def has_ticket_link(self, obj):
        """Display if show has ticket link"""
        return bool(obj.ticket_link)
    has_ticket_link.boolean = True
    has_ticket_link.short_description = 'Tickets Available'
    
    def is_past(self, obj):
        """Display if show is in the past"""
        return obj.is_past
    is_past.boolean = True
    is_past.short_description = 'Past Show'
