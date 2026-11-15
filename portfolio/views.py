from rest_framework import generics
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .models import ContactMessage, JourneyItem, Project, Skill, SiteProfile
from .serializers import (ContactMessageSerializer, JourneyItemSerializer, ProfileSerializer,
                          ProjectSerializer, SkillSerializer)


class ProfileView(APIView):
    def get(self, request):
        profile = SiteProfile.objects.prefetch_related("stats").first()
        if profile is None:
            return Response({"detail": "Profile not created yet."}, status=404)
        return Response(ProfileSerializer(profile).data)


class ProjectList(generics.ListAPIView):
    serializer_class = ProjectSerializer
    pagination_class = None
    queryset = Project.objects.filter(is_published=True).prefetch_related("images")


class SkillList(generics.ListAPIView):
    serializer_class = SkillSerializer
    pagination_class = None
    queryset = Skill.objects.filter(is_visible=True)


class JourneyList(generics.ListAPIView):
    serializer_class = JourneyItemSerializer
    pagination_class = None
    queryset = JourneyItem.objects.all()


class ContactCreate(generics.CreateAPIView):
    """POST name, email, message. Limited to 5 messages/hour per visitor."""
    serializer_class = ContactMessageSerializer
    queryset = ContactMessage.objects.all()
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "contact"
