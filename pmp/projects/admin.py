from django.contrib import admin
from . models import Project, Plan, Space, PlanSpace, Equipment, Furniture

class PlanInline(admin.TabularInline):
    model = Plan
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [PlanInline]
    list_display = ("name", "type", "created_by", "creation_date", "finish_date", "status")
    list_filter = ("type", "creation_date", "status")
    search_fields = ("name", "type")
    readonly_fields = ("created_by", "creation_date", "finish_date", "assigned_to")
    ordering = ("-creation_date",) 

class SpaceInline(admin.TabularInline):
    model = PlanSpace
    extra = 1

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    inlines = [SpaceInline]
    list_display = ("reference_name", "description", "status", "project")
    search_fields = ("reference_name",)
    ordering = ("reference_name",)

@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "status")
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("name", "requirement")
    search_fields = ("name",)

@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ("name", "requirement")
    search_fields = ("name",)
