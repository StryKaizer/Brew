from brew.models import MashingScheme, MashingStep, Batch, MashLog, Variable
from django.contrib import admin







class MashingStepInline(admin.TabularInline):
    verbose_name = 'Mashing Step'
    model = MashingStep
    extra = 1


class MashingSchemeAdmin(admin.ModelAdmin):
    fieldsets = [
        
        ('Basic brew info', {'fields': ['name']}),
    ]
    inlines = [MashingStepInline]

admin.site.register(MashingScheme, MashingSchemeAdmin)
admin.site.register(Batch)
admin.site.register(Variable)
admin.site.register(MashLog)