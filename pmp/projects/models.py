from django.db import models
from django.conf import settings

class Project(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("reviewed", "Reviewed"),
        ("approved", "Approved"),
    ]

    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_projects')
    creation_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(blank=True, null=True)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assigned_projects')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name

class Plan(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("submitted", "Submitted"),
    ]
    reference_name = models.CharField(max_length=50)
    description = models.TextField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='plans')

    def __str__(self):
        return self.reference_name

class Space(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("submitted", "Submitted"),
    ]
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    plans = models.ManyToManyField(Plan, through="PlanSpace", related_name="spaces")

    def __str__(self):
        return self.name
    
class PlanSpace(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="plan_spaces")
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="space_plans")
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.plan.reference_name} - {self.space.name} (x{self.count})"


class Equipment(models.Model):
    name = models.CharField(max_length=50)
    requirement = models.TextField(max_length=255)

    def __str__(self):
        return self.name

class Furniture(models.Model):
    name = models.CharField(max_length=50)
    requirement = models.TextField(max_length=255)

    def __str__(self):
        return self.name

class SpaceEquipment(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class SpaceFurniture(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
