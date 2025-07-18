from django.contrib import admin
from . import models

class InformationAdmin(admin.StackedInline):
    model = models.Information

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','price')
    inlines = (InformationAdmin,)    

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('title','slug','parent')
    prepopulated_fields = {'slug':('title',)}

admin.site.register(models.Color)
admin.site.register(models.Size)
admin.site.register(models.Information)

class InformationjobAdmin(admin.StackedInline):
    model = models.Informationjob

@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title','price')
    inlines = (InformationjobAdmin,)