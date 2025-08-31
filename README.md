                        # Alx_Capstone_Project Progress & Walk-Through Documentation #

Week 2:

- Done setting up Remote and Local repositories.
- Done setting up a virtual environment.
- Done Setting up essential files like: (.gitignore), (reuirements.txt.).
- Created a new branch specialized for starting core apps.
- Created core structure apps.

Week 3:
- Created all apps' models and relations.
- Created a CustomUser model.
- Registered CustomUser in Settings.py and admin.py
- Tested Admin Panel's user editing and creation.

Week 4:
- Revising Admin Panel planning for models to be edited by Admins.

Week 5:
- Registered all projects app's modelsinto the admin panel.
- Customized list_display, search_filter, readonly_fields, ordering, ...
- Merged (feature/apps-setup) branch with (main).
- Created new (feature/permissions) branch. 
- Created all API Endpoints Viwes.
- Added two more serializers for CEO and PM assigning users.
- Performed several test using postman.
- Updated both accounts and projects' views(API endpoints) tomatch url paths.
- prepared some ready-to-take postman environments for presentation.

=======================================


PMP - ALX Capstone Project:

- PMP is composed of two parts, Admin and User side.
    * Admin Part:
        # Controled in accounts/ app.
        # In models.py:
                CustomUser model.
        # Creating users. (Admin Panel)
        # Creating Projects. (project -> plans -> spaces) in (Admin Panel)
        # Updating Equipment & Furniture Catalogs. (Admin Panel)
        # In Views.py:
                LoginAPIView: Endpoint for users login, validation and token generation.
                UserListAPIView: Endpoint for listing all users.
                UserRetrieveAPIView: Endpoint for retrieving a specific user.
                UserUpdateAPIView: Endpoint for CEO to change users' roles.
    
    * User Part:
        # Controled in projects/ app.
        # in models.py:
                Project, Plan, Space, Equipment, Furniture (core models).
                PlanSpace, SpaceEquipment, SpaceFurniture (joint models).
        # Users manipulate data through API endpoints in views.py.
        # Each user has certain features depending on their role (CEO, PM-> Project Manager, Tl-> Team Leader, Planner).
        # Equipment and Furniture models are registered in admin.py, so admins update it in Admin Panel.
        # in serializers.py : 
                ProjectSerializer, ProjectCEOAssignmentSerializer, ProjectPMAssignmentSerializer, PlanSerializer, 
                SpaceSerializer, SpaceEquipmentSerializer and SpaceFurnitureSerializer
        # In Views.py:
                ProjectListAPIView: Responsible for listing all projects (varies depending on the role of user)
                ProjectRetrieveAPIView: Responsible for listing a project (varies depending on the role of user)
                ProjectCEOAssignmentView: CEO feature to assign PMs & Consultants to projects.
                ProjectPMAssignmentView: PM feature to assign TLs & Planners to projects.
                ProjectApproveView: CEO feature to mark projects [Approved].
                ProjectReviewView: Consultants feature to mark projects [Reviewed].
                PlanSubmitView: TLs feature to mark plans [Submitted] can't be submitted unless all spaces linked to a plan submitted.
                SpaceSubmitView: Planners feature to mark spaces [Submitted].
                SpaceEquipmentUpdateView: Planners feature to assign/choose Equipment to a space. (from catalogs)
                SpaceFurnitureUpdateView: Planners feature to assign/choose Furniture to a space. (from catalogs)

- General Configurations:
    * All endpoints/API-Views are protected by IsAuthenticated and Token generation.
    * Settings.py:
        # All apps are registered in INSTALLED_APPS.
        # rest_framewrok + rest_framework.authtoken are registered in INSTALLED_APPS.
        # DRF Configuration:
                REST_FRAMEWORK = {
                                    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
                                     'PAGE_SIZE': 10, #Global Pagination
                                     'DEFAULT_AUTHENTICATION_CLASSES': [
                                       'rest_framework.authentication.TokenAuthentication', #Token Authentication
                                     ],
                                }
        # User Authentication:
                AUTH_USER_MODEL = "accounts.CustomUser"
    * url.py:
        # API endpoints are included within url_patterns.
                urlpatterns = [
                                path('admin/', admin.site.urls),
                                path('api/', include('projects.urls')),
                                path('api/accounts/', include('accounts.urls')),
                            ]

- Projects requirments and environment:
    * A file called requirements.txt always updated with all installed frameworks and libraries.
        # pip freeze > requirments.txt
    * You can install all requirements to safely and successfully operate the project.
        # pip install -r requirements.txt


- Future expantion and ideas:
    * PDF generating integration.
    * Comments and Notes features.
    * Exapnding the project to include non-medical spaces.
    * Expanding system's users range to include more positions.

=====================================

Deployment Branch

Live API Endpoints

- The backend API is hosted locally and exposed publicly via ngrok. This allows reviewers to access your Django API even though it runs on your machine.

ngrok:

- ngrok is a tool that creates a secure public URL for your local server.
- It forwards internet traffic to your local Django server, so reviewers can test endpoints without needing to deploy to a cloud service.
- Free ngrok URLs are temporary and change every time you restart the tunnel.

Configuring ngrok:

- Install  through website: 
 #      https://ngrok.com/

- Start the Django server locally:
#       python manage.py runserver 8000

- Open a new terminal and start ngrok:
#       ngrok http 8000

- Copy the Forwarding HTTPS URL provided by ngrok (e.g., https://8cd4163424a5.ngrok-free.app)
- Use this URL for all API requests instead of http://127.0.0.1:8000.
- Keep both Django server and ngrok running while testing. Once stopped, the URL will no longer work.



Endpoints

- Get Project Details
#   GET https://8cd4163424a5.ngrok-free.app/api/projects/1/

- Update Space Furniture
#  PATCH https://8cd4163424a5.ngrok-free.app/api/projects/1/plans/2/spaces/1/furnitures/1/update/


- Request body example (JSON):

            {
            "space_id": 1,
            "furniture_id": 1,
            "quantity": 10
            }


Authentication

- The API uses Token Authentication.
- Include your token in the Authorization header:
#    Authorization: Token <your-token-here>

- Example header in Postman:
#    Key: Authorization          Value: Token 1234567890abcdef1234567890abcdef



Additional Notes

- Deployment work all in (deployment) branch, so it's not merged into (main) branch for clarity.
- ngrok URLs are temporary; they change every time the tunnel restarts.
- CSRF errors may occur if accessing Django admin via ngrok — use your local server instead (http://127.0.0.1:8000/admin/).
- Users should only test the API endpoints using the ngrok URL + token.

