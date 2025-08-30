from django.urls import path
from . import views

urlpatterns = [

    path("projects/", views.ProjectListAPIView.as_view(), name="project-list"),
    path("projects/<int:id>/", views.ProjectRetrieveAPIView.as_view(), name="project-detail"),
    path("projects/<int:pk>/assign-ceo/", views.ProjectCEOAssignmentView.as_view(), name="project-assign-ceo"),
    path("projects/<int:pk>/assign-pm/", views.ProjectPMAssignmentView.as_view(), name="project-assign-pm"),
    path("projects/<int:pk>/approve/", views.ProjectApproveView.as_view(), name="project-approve"),
    path("projects/<int:pk>/review/", views.ProjectReviewView.as_view(), name="project-review"),

    path("projects/<int:project_id>/plans/<int:pk>/submit/", views.PlanSubmitView.as_view(), name="plan-submit"),

    path("projects/<int:project_id>/plans/<int:plan_id>/spaces/<int:pk>/submit/", views.SpaceSubmitView.as_view(), name="space-submit"),

    path(
        "projects/<int:project_id>/plans/<int:plan_id>/spaces/<int:space_id>/equipments/<int:pk>/update/",
        views.SpaceEquipmentUpdateView.as_view(),
        name="space-equipment-update"
    ),

    path(
        "projects/<int:project_id>/plans/<int:plan_id>/spaces/<int:space_id>/furnitures/<int:pk>/update/",
        views.SpaceFurnitureUpdateView.as_view(),
        name="space-furniture-update"
    ),
]
