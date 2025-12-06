from django.urls import path
from .views import *
from django.urls import path, include




urlpatterns = [
    path("liste/", ConferenceList.as_view(), name="conference_liste"),
    path("details/<int:pk>", ConferenceDetails.as_view(), name="conference_detail"),
    path("forms/", ConferenceCreate.as_view(), name="conference_add"),
    path("<int:pk>/edit/", ConferenceCreate.as_view(), name="conference_edit"),
    path("<int:pk>/delete/", ConferenceDelete.as_view(), name="conference_delete"),

    # 🔽 Mets cette ligne avant celle avec <str:pk>
    path('submission/add/', AddSubmission.as_view(), name='add_submission'),
    path("submissions/", ListeSubmissions.as_view(), name="list_submissions"),
    path('submission/<str:pk>/edit/', UpdateSubmission.as_view(), name='update_submission'),
    path("submission/<str:pk>/", SubmissionDetail.as_view(), name="submission_detail"),
]
