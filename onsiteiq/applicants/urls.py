from applicants import views as applicant_views
from django.urls import path


urlpatterns = [
    path("login/", applicant_views.login),
    path("create/", applicant_views.create),
    path("view_all/", applicant_views.view_all),
    path("view/<str:unique_id>/", applicant_views.view_one),
    path("note/<str:unique_id>/", applicant_views.update_note),
    path("approve_reject/<str:unique_id>/", applicant_views.approve_reject)
]
