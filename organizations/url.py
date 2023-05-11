from django.urls import path

from . import views, views_admin

admin_urls = [
    path(
        "admin_dashboard/<str:uuid>/",
        views_admin.admin_dashboard,
        name="admin_dashboard",
    ),
    path("admin_myteam/<str:uuid>/", views_admin.admin_myteam, name="admin_myTeam"),
    path(
        "admin_new_members/<str:uuid>/",
        views_admin.new_members,
        name="new_member_list",
    ),
    path(
        "admin_team/profile/<str:uuid>/<str:account_uuid>",
        views_admin.admin_member_profile,
        name="admin_member_profile",
    ),
    path("admin_roles/<str:uuid>/", views_admin.admin_roles, name="admin_roles"),
    path(
        "admin_rolesform/<str:uuid>/",
        views_admin.admin_roles_form,
        name="admin_rolesfrom",
    ),
    path("admin_issues/<str:uuid>/", views_admin.admin_issues, name="admin_issues"),
    path("admin_issuesdetails/<str:uuid>/<int:issue_pk>", views_admin.admin_IssueDetails, name="admin_issues_details"),
]


urlpatterns = [
    path("dashboard/<str:uuid>/", views.dashboard, name="dashboard"),
    path("roles/<str:uuid>/", views.roles, name="roles"),
    path("myteam/<str:uuid>/", views.myteam, name="my_team"),
    path("reports/<str:uuid>/", views.reports, name="reports"),
    path("profile/<str:uuid>/", views.profile, name="profile"),
    path("issues/<str:uuid>/", views.issues, name="issues"),
    path(
        "issues/details/<str:uuid>/<int:issue_pk>",
        views.getIssueDetails,
        name="issues details",
    ),
    path("raiseIssue/<str:uuid>/", views.raiseIssue, name="raiseIssue"),
    path("redirect/dashboard", views.dashboard_redirect, name="dashboard redirect"),
] + admin_urls
