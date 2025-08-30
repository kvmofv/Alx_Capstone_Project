from rest_framework import serializers
from .models import Project, Plan, Space, SpaceEquipment, SpaceFurniture, Equipment, Furniture
from accounts.models import CustomUser

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ["name", "requirement"]
        
class FurnitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furniture
        fields = ["name", "requirement"]

class SpaceSerializer(serializers.ModelSerializer):
    spaces = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Space
        fields = ["name", "description", "status", "spaces"]

class SpaceEquipmentSerializer(serializers.ModelSerializer):
    space_id = serializers.PrimaryKeyRelatedField(queryset=Space.objects.all(), source="space", write_only=True)
    space = serializers.StringRelatedField(read_only=True)
    equipment = EquipmentSerializer(read_only=True)
    equipment_id = serializers.PrimaryKeyRelatedField(queryset=Equipment.objects.all(), source="equipment", write_only=True)

    class Meta:
        model = SpaceEquipment
        fields = ["space", "equipment", "equipment_id", "quantity"]

class SpaceFurnitureSerializer(serializers.ModelSerializer):
    space_id = serializers.PrimaryKeyRelatedField(queryset=Space.objects.all(), source="space", write_only=True)
    space = serializers.StringRelatedField(read_only=True)
    furniture = FurnitureSerializer(read_only=True)
    furniture_id = serializers.PrimaryKeyRelatedField(queryset=Furniture.objects.all(), source="furniture", write_only=True)

    class Meta:
        model = SpaceFurniture
        fields = ["space", "furniture", "furniture_id", "quantity"]

class PlanSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(read_only=True)
    spaces = SpaceSerializer(many=True, read_only=True)

    class Meta:
        model = Plan
        fields = ["reference_name", "description", "status", "project", "spaces"]

class ProjectSerializer(serializers.ModelSerializer):
    plans = PlanSerializer(many=True, read_only=True)
    assigned_to = serializers.StringRelatedField(many=True, read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "type", "created_by", "creation_date", "finish_date", "assigned_to", "status", "plans"]

class ProjectCEOAssignmentSerializer(serializers.ModelSerializer):
    user_ids = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role__in=["PM", "Consultant"]),
        many=True,
        write_only=True
    )

    class Meta:
        model = Project
        fields = ["id", "user_ids"]

    def update(self, instance, validated_data):
        users = validated_data.pop("user_ids", [])
        instance.assigned_to.set(users) 
        instance.save()
        return instance


class ProjectPMAssignmentSerializer(serializers.ModelSerializer):
    user_ids = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role__in=["Tl", "Planner"]),
        many=True,
        write_only=True
    )

    class Meta:
        model = Project
        fields = ["id", "user_ids"]

    def update(self, instance, validated_data):
        users = validated_data.pop("user_ids", [])
        instance.assigned_to.set(users)
        instance.save()
        return instance

