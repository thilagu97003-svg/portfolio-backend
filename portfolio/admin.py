from django.contrib import admin
from django.utils.html import format_html

from .models import AboutItem, ContactMessage, JourneyItem, Project, ProjectImage, Skill, SiteProfile, Stat


class StatInline(admin.TabularInline):
    model = Stat
    extra = 0
class AboutItemInline(admin.TabularInline):
    model = AboutItem
    extra = 1
    fields = ("kind", "title", "description", "order")


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    inlines = [StatInline, AboutItemInline]
    list_display = ["full_name", "role", "email", "available_for_hire"]

    def has_add_permission(self, request):
        return not SiteProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["preview", "title", "badge", "order", "is_published"]
    list_display_links = ["preview", "title"]
    list_editable = ["order", "is_published"]
    list_filter = ["badge", "is_published"]
    search_fields = ["title", "description", "tech_stack"]
    inlines = [ProjectImageInline]

    @admin.display(description="Image")
    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:6px">', obj.image.url)
        return "-"


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "icon", "color", "order", "is_visible"]
    list_editable = ["category", "order", "is_visible"]
    list_filter = ["category", "is_visible"]
    search_fields = ["name"]


@admin.register(JourneyItem)
class JourneyItemAdmin(admin.ModelAdmin):
    list_display = ["title", "organization", "kind", "period", "order"]
    list_editable = ["order"]
    list_filter = ["kind"]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created_at", "is_read"]
    list_editable = ["is_read"]
    list_filter = ["is_read"]
    search_fields = ["name", "email", "message"]
    readonly_fields = ["name", "email", "message", "created_at"]

    def has_add_permission(self, request):
        return False
