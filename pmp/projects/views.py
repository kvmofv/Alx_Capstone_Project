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

        if request.user.role != "CEO":
            return Response({"error": "Access Denied."}, status=403)

        new_status = request.data.get("status")
        if new_status not in ["approved", "reviewed"]:
            return Response({"error": "Invalid status."}, status=400)

        project.status = new_status
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

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        return Plan.objects.filter(project_id=project_id)

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

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        plan_id = self.kwargs.get("plan_id")
        return Space.objects.filter(plans__id=plan_id, plans__project_id=project_id)

    def update(self, request, *args, **kwargs):
        space = self.get_object()

        project_id = self.kwargs.get("project_id")
        plan_id = self.kwargs.get("plan_id")

        
        project = space.plans.filter(id=plan_id, project_id=project_id).first()
        if not project:
            return Response({"error": "Invalid project or plan."}, status=404)

        if project.status == "approved":
            return Response({"error": "Project Locked After Approval."}, status=403)

        if request.user.role != "Planner":
            return Response({"error": "Planner's Duty."}, status=403)

        space.status = "submitted"
        space.save()

        return Response(self.get_serializer(space).data, status=200)

class SpaceEquipmentUpdateView(generics.UpdateAPIView):
    queryset = SpaceEquipment.objects.all()
    serializer_class = SpaceEquipmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        plan_id = self.kwargs.get("plan_id")
        space_id = self.kwargs.get("space_id")

        return SpaceEquipment.objects.filter(
            space_id=space_id,
            space__plans__id=plan_id,
            space__plans__project__id=project_id
        )

    def update(self, request, *args, **kwargs):
        spaceequipment = self.get_object()

        project_id = self.kwargs.get("project_id")
        plan_id = self.kwargs.get("plan_id")


        plan = spaceequipment.space.plans.filter(id=plan_id, project_id=project_id).first()
        if not plan:
            return Response({"error": "Invalid project/plan combination."}, status=404)

        project = plan.project

        if project.status == "approved":
            return Response({"error": "Project Locked After Approval."}, status=403)

        if request.user.role not in ["PM", "TL", "Planner"]:
            return Response({"error": "Access Denied."}, status=403)

        quantity = int(request.data.get("quantity", 0))
        spaceequipment.quantity = quantity
        spaceequipment.save()

        return Response(self.get_serializer(spaceequipment).data, status=200)

        
class SpaceFurnitureUpdateView(generics.UpdateAPIView):
    queryset = SpaceFurniture.objects.all()
    serializer_class = SpaceFurnitureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        plan_id = self.kwargs.get("plan_id")
        space_id = self.kwargs.get("space_id")

        return SpaceFurniture.objects.filter(
            space_id=space_id,
            space__plans__id=plan_id,
            space__plans__project__id=project_id
        )

    def update(self, request, *args, **kwargs):
        spacefurniture = self.get_object()

        project_id = self.kwargs.get("project_id")
        plan_id = self.kwargs.get("plan_id")


        plan = spacefurniture.space.plans.filter(id=plan_id, project_id=project_id).first()
        if not plan:
            return Response({"error": "Invalid project/plan combination."}, status=404)

        project = plan.project

        if project.status == "approved":
            return Response({"error": "Project Locked After Approval."}, status=403)

        if request.user.role not in ["PM", "TL", "Planner"]:
            return Response({"error": "Access Denied."}, status=403)

        quantity = int(request.data.get("quantity", 0))
        spacefurniture.quantity = quantity
        spacefurniture.save()

        return Response(self.get_serializer(spacefurniture).data, status=200)