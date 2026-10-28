from django.urls import path
from . import api_views, views

app_name = "courses"

urlpatterns = [
    # Web UI Routes
    path("", views.course_list_view, name="course-list"),
    path("courses/create/", views.course_create_view, name="course-create"),
    path("courses/<int:pk>/edit/", views.course_edit_view, name="course-edit"),
    path("courses/<int:pk>/delete/", views.course_delete_view, name="course-delete"),

    # RESTful API Routes
    path("api/courses/", api_views.api_course_list, name="api-course-list"),
    path("api/courses/<int:pk>/", api_views.api_course_detail, name="api-course-detail"),
]
