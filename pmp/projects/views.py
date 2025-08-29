from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import (
    ProjectSerializer, 
    ProjectCEOAssignmentSerializer, 
    ProjectPMAssignmentSerializer, 
    PlanSerializer, 
    SpaceSerializer, 
    SpaceEquipmentSerializer, 
    SpaceFurnitureSerializer
    )
from .models import Project, Plan, Space, SpaceFurniture, SpaceEquipment


class ProjectListAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role in ("PM", "CONSULTANT", "TL", "PLANNER"):
            return Project.objects.filter(assigned_to=user)

        if user.role == "CEO":
            return Project.objects.all()

        return Project.objects.none()

class ProjectRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user

        if user.role == "CEO":
            return Project.objects.all()

        return Project.objects.filter(assigned_to=user)

class ProjectCEOAssignmentView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCEOAssignmentSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        project = self.get_object()

        if project.status == "approved":
            return Response({"error": "Project is Locked After Approval."}, status=403)

        if request.user.role != "CEO":
            return Response({"error": "Access Denied."}, status=403)

        return super().update(request, *args, **kwargs)

class ProjectPMAssignmentView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectPMAssignmentSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        project = self.get_object()

        if project.status == "approved":
            return Response({"error": "Project is Locked After Approval."}, status=403)

        if request.user.role != "PM":
            return Response({"error": "Access Denied."}, status=403)

        return super().update(request, *args, **kwargs)

class ProjectApproveView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        project = self.get_object()

        if project.status == "approved":
            return Response({"error": "Project Locked After Approval. "}, status=403)
        
        if request.user.role != "CEO":
            return Response({"error": "Access Denied. "}, status=403)
        
        project.status = "approved"
        project.save()

        return Response(self.get_serializer(project).data, status=200)

class ProjectReviewView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        project = self.get_object()

        if project.status == "approved":
            return Response({"error": "Project Locked After Approval. "}, status=403)
        
        if request.user.role != "CONSULTANT":
            return Response({"error": "Consultant's Duty. "}, status=403)
        
        project.status = "reviewed"
        project.save()

        return Response(self.get_serializer(project).data, status=200)

class PlanSubmitView(generics.UpdateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        plan = self.get_object()
        project = plan.project

        if project.status == "approved":
            return Response({"error": "Project Locked After Approval. "}, status=403)
        
        if request.user.role != "TL":
            return Response({"error": "TL's Duty. "}, status=403)
        
        plan.status = "submitted"
        plan.save()

        return Response(self.get_serializer(plan).data, status=200)

class SpaceSubmitView(generics.UpdateAPIView):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        space = self.get_object()
        project = space.plans.project

        if project.status == "approved":
            return Response({"error": "project Locked After Approval. "}, status=403)
        
        if request.user.role != "PLANNER":
            return Response({"error": "planner's Duty. "}, status=403)
        
        space.status = "submitted"
        space.save()

        return Response(self.get_serializer(space).data, status=200)

class SpaceEquipmentUpdateView(generics.UpdateAPIView):
    queryset = SpaceEquipment.objects.all()
    serializer_class = SpaceEquipmentSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        spaceequipment = self.get_object()
        project = spaceequipment.space.plans.project

        if project.status == "approved":
            return Response({"error": "Project Locked After Approval. "}, status=403)
        
        if request.user.role not in ["PM", "TL", "PLANNER"]:
            return Response({"error": "Access Denied. "}, status=403)
        
        quantity = int(request.data.get("quantity", 0))
        spaceequipment.quantity += quantity
        spaceequipment.save()

        return Response(self.get_serializer(spaceequipment).data, status=200)
    
class SpaceFurnitureUpdateView(generics.UpdateAPIView):
    queryset = SpaceFurniture.objects.all()
    serializer_class = SpaceFurnitureSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        spacefurniture = self.get_object()
        project = spacefurniture.space.plans.project

        if project.status == "approved":
            return Response({"error": "Project Locked After Approval. "}, status=403)
        
        if request.user.role not in ["PM", "TL", "PLANNER"]:
            return Response({"error": "Access Denied. "}, status=403)
        
        quantity = int(request.data.get("quantity", 0))
        spacefurniture.quantity += quantity
        spacefurniture.save()

        return Response(self.get_serializer(spacefurniture).data, status=200)