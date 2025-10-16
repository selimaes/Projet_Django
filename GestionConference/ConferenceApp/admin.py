
from django.contrib import admin
from .models import Conference, Submission







admin.site.register(Submission)
admin.site.site_header="Conference Managment admin"
admin.site.site_title="conference dashboard"

@admin.register(Conference)
class AdminPerso(admin.ModelAdmin):
    list_display =("name","theme","location","start_date","end_date")
    ordering=("start_date",)
    list_filter =("theme",)
    search_fields =("name" ,)
    
    fieldsets = (
    ("information generale", {
        "fields": ("conference_id", "name", "theme", "description")  # tuple ici
    }),
    ("Logistics", {
        "fields": ("location", "start_date", "end_date")  # tuple ici aussi
    }),
)
