from django.contrib import admin
from .models import Conference,Submission

admin.site.site_header = "Conference Management Admin"
admin.site.site_title = "Conference Dashboard"
admin.site.index_title = "Welcome to Conference Management Admin"

admin.site.register(Submission)

# Register your models here.


class submissionTabInline(admin.TabularInline):
    model = Submission   
    extra = 1            
    readonly_fields = ('submission_id',)
    #fields = ('title','keywords','payed','user_id','submission_date')
    can_delete = False
    show_change_link = True
   
    
    
class submissionStackInline(admin.StackedInline):
    model = Submission    
    extra = 1             
    readonly_fields = ('submission_id',)
    #fields = ('title','keywords','payed','user_id','submission_date')
    can_delete = False
    show_change_link = True
    
    
@admin.register(Conference)

class AdminPerson(admin.ModelAdmin):
    list_display = ('name','location','start_date', 'end_date','theme','duration')
    ordering = ('-start_date',) 
    search_fields = ('name', 'theme')
    list_filter = ('theme', 'start_date')
    date_hierarchy = 'start_date'
    fieldsets = (
     ("Gneral Information",{
         'fields':('name','description','theme')
                            }),   
        ("Logistics",{
            'fields':('location','start_date','end_date')
                            }),   
    )
    readonly_fields = ('conference_id',)
    
    inlines = [submissionStackInline]
    
    def duration(self,obj):
        
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days + 1  
        return 'N/A'
    
    duration.short_description = 'Duration (days)'

@admin.action(description='mark_as_payed')
def mark_as_payed(modeladmin,req,queryset):
    queryset.update(payed=True)

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'status','submission_date', 'payed', 'short_abstract')
    list_editable = ('status', 'payed')
    ordering = ('-submission_date',)
    search_fields = ('title', 'keywords')
    list_filter = ('status', 'payed', 'submission_date')
    
    fieldsets = (
        ("General Information", {
            'fields': ('submission_id', 'title', 'abstract', 'keywords')
        }),
        ("File and Conference", {
            'fields': ('paper', 'conference_id')
        }),
        ("Tracking", {
            'fields': ('status', 'payed', 'user_id')
        }),
    )
    
    readonly_fields = ('submission_id',)
    actions=[mark_as_payed]

    
    def short_abstract(self, obj):
        """Truncate abstract JUSQU A  50 characters """
        if obj.abstract:
            return obj.abstract[:50] + '...' if len(obj.abstract) > 50 else obj.abstract
        return '-'
    short_abstract.short_description = 'Abstract Preview'
    
admin.site.unregister(Submission)
admin.site.register(Submission, SubmissionAdmin)
