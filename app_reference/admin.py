from django.contrib import admin
from .models import *


class OfficesAdmin(admin.ModelAdmin):
    list_display = ['name', 'short']


class IDTypesAdmin(admin.ModelAdmin):
    list_display = ['type', 'office']


class DepartmentsAdmin(admin.ModelAdmin):
    list_display = ['dept']


class StrandsAdmin(admin.ModelAdmin):
    list_display = ['strand']


class CoursesAdmin(admin.ModelAdmin):
    search_fields = ['course']
    list_display = ['course']


class LevelsAdmin(admin.ModelAdmin):
    list_display = ['level']


class CardsLayoutAdmin(admin.ModelAdmin):
    list_display = ['layout_name']


class EmploymentTypesAdmin(admin.ModelAdmin):
    list_display = ['emp_type']


admin.site.register(Offices, OfficesAdmin)
admin.site.register(IDTypes, IDTypesAdmin)
admin.site.register(Departments, DepartmentsAdmin)
admin.site.register(Strands, StrandsAdmin)
admin.site.register(Courses, CoursesAdmin)
admin.site.register(Levels, LevelsAdmin)
admin.site.register(CardsLayout, CardsLayoutAdmin)
admin.site.register(EmploymentTypes, EmploymentTypesAdmin)
