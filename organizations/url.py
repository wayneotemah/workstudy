from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/<str:uuid>/' ,views.dashboard, name='dashboard'),
    path('roles/<str:uuid>/' ,views.roles, name='roles'),
    path('myteam/<str:uuid>/' ,views.myteam, name='my_team'),
    path('reports/<str:uuid>/' ,views.reports, name='reports'),
    path('profile/<str:uuid>/' ,views.profile, name='profile'),
    path('issues/<str:uuid>/' ,views.issues, name='issues'),
    path('issues/details/<str:uuid>/<int:issue_pk>' ,views.getIssueDetails, name='issues details'),
    path('raiseIssue/<str:uuid>/' ,views.raiseIssue, name='raiseIssue'),
    path('redirect/dashboard',views.dashboard_redirect, name= "dashboard redirect"),
]