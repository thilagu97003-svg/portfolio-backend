from rest_framework import serializers

from .models import ContactMessage, JourneyItem, Project, Skill, SiteProfile


def file_url(request, f):
    """Absolute URL for local media; Cloudinary already returns a full URL."""
    if not f:
        return None
    url = f.url
    return request.build_absolute_uri(url) if url.startswith("/") else url


class ProjectSerializer(serializers.ModelSerializer):
    # camelCase keys so the React code matches the old projectsData.js shape
    techStack = serializers.SerializerMethodField()
    liveDemo = serializers.CharField(source="live_url", read_only=True)
    github = serializers.CharField(source="github_url", read_only=True)
    image = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    gallery = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ["id", "title", "description", "features", "techStack", "badge",
                  "image", "liveDemo", "github", "gallery"]

    def get_techStack(self, obj):
        return [t.strip() for t in obj.tech_stack.split(",") if t.strip()]

    def get_features(self, obj):
        return [line.strip() for line in obj.features.splitlines() if line.strip()]

    def get_image(self, obj):
        return file_url(self.context["request"], obj.image)

    def get_gallery(self, obj):
        request = self.context["request"]
        return [{"url": file_url(request, i.image), "caption": i.caption} for i in obj.images.all()]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name", "category", "icon", "color"]


class JourneyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneyItem
        fields = ["id", "kind", "title", "organization", "period", "description", "badge"]


class ProfileSerializer(serializers.ModelSerializer):
    displayName = serializers.CharField(source="display_name")
    fullName = serializers.CharField(source="full_name")
    githubUrl = serializers.CharField(source="github_url")
    linkedinUrl = serializers.CharField(source="linkedin_url")
    workMode = serializers.CharField(source="work_mode")
    availableForHire = serializers.BooleanField(source="available_for_hire")
    stats = serializers.SerializerMethodField()
    about = serializers.SerializerMethodField()

    class Meta:
        model = SiteProfile
        fields = ["displayName", "fullName", "initials", "role", "tagline", "bio", "email",
                  "githubUrl", "linkedinUrl", "location", "workMode", "availableForHire", "stats", "about"]

    def get_stats(self, obj):
        return [{"value": s.value, "label": s.label} for s in obj.stats.all()]
    def get_about(self, obj):
        items = list(obj.about_items.all())

        def titles(kind):
            return [i.title for i in items if i.kind == kind]

        return {
            "heading": obj.about_heading,
            "intro": obj.about_intro,
            "body": obj.about_body,
            "badges": titles("badge"),
            "highlights": titles("highlight"),
            "philosophy": titles("philosophy"),
            "whyHire": [
                {"title": i.title, "description": i.description}
                for i in items if i.kind == "why_hire"
            ],
        }

    


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]

    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Please enter your name (min 3 characters).")
        return value.strip()

    def validate_message(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters long.")
        return value.strip()
