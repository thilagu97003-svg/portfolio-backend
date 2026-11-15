from django.urls import path

from . import views

urlpatterns = [
    path("profile/", views.ProfileView.as_view()),
    path("projects/", views.ProjectList.as_view()),
    path("skills/", views.SkillList.as_view()),
    path("journey/", views.JourneyList.as_view()),
    path("contact/", views.ContactCreate.as_view()),
]
