from brew.models import Brew, MashingSchemeItem, BrewingDay, MashingTempLog
from django.contrib import admin







class MashingSchemeItemInline(admin.TabularInline):
    verbose_name = 'Mashing Scheme Item'
    model = MashingSchemeItem
    extra = 1


class BrewAdmin(admin.ModelAdmin):
    fieldsets = [
        
        ('Basic brew info', {'fields': ['name']}),
    ]
    inlines = [MashingSchemeItemInline]

admin.site.register(Brew, BrewAdmin)
admin.site.register(BrewingDay)
admin.site.register(MashingTempLog)