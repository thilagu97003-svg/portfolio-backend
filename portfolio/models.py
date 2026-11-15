from django.db import models


class SiteProfile(models.Model):
    """Single record: your name, role and contact links (used in Hero, Navbar, Footer, Contact, Terminal)."""

    display_name = models.CharField(max_length=60, help_text="Short name in the hero, e.g. Thilak")
    full_name = models.CharField(max_length=100, help_text="Shown in the navbar, e.g. K. Thilagavathi")
    initials = models.CharField(max_length=4, default="KT")
    role = models.CharField(max_length=100, default="Frontend Developer")
    tagline = models.TextField(help_text="The paragraph under your role in the hero")
    bio = models.TextField(blank=True, help_text="Short bio used by the terminal 'bio' command")
    email = models.EmailField()
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    work_mode = models.CharField(max_length=150, blank=True)
    available_for_hire = models.BooleanField(default=True, help_text="Shows the green 'Available for Hire' badge")

    about_heading = models.CharField(
        max_length=200, default="Transitioning with Passion into Full Stack Development"
    )
    about_intro = models.TextField(
        blank=True,
        default="With 4+ years of professional background across Quality Control and Academic Lecturing, I developed high attention to detail, structured problem-solving, and clear communication.",
        help_text="First paragraph of the About section",
    )
    about_body = models.TextField(
        blank=True,
        default="I build complete web and mobile applications, from responsive React and React Native interfaces to Django REST APIs and PostgreSQL databases, using **HTML5, CSS3, JavaScript, Bootstrap 5, React.js, Python,** and **Django**.",
        help_text="Second paragraph. Put **double stars** around words you want in bold",
    )

    class Meta:
        verbose_name = "Site profile"
        verbose_name_plural = "Site profile"

    def save(self, *args, **kwargs):
        self.pk = 1  # only ever one profile
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name


class Stat(models.Model):
    profile = models.ForeignKey(SiteProfile, on_delete=models.CASCADE, related_name="stats")
    value = models.CharField(max_length=20, help_text="e.g. 7+")
    label = models.CharField(max_length=40, help_text="e.g. Live Apps")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.value} {self.label}"

class AboutItem(models.Model):
    KINDS = [
        ("badge", "Badge under the paragraphs"),
        ("highlight", "Quick Highlight"),
        ("why_hire", "Why Hire Me point"),
        ("philosophy", "Core Philosophy tag"),
    ]
    profile = models.ForeignKey(SiteProfile, on_delete=models.CASCADE, related_name="about_items")
    kind = models.CharField(max_length=12, choices=KINDS)
    title = models.CharField(max_length=150, help_text="Badge/tag text, or the heading of a Why Hire Me point")
    description = models.TextField(blank=True, help_text="Only used for Why Hire Me points")
    order = models.PositiveIntegerField(default=0, help_text="Lower number shows first")

    class Meta:
        ordering = ["kind", "order", "id"]

    def __str__(self):
        return f"{self.get_kind_display()}: {self.title}"


class Project(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    features = models.TextField(blank=True, help_text="One feature per line (shown in the details popup)")
    tech_stack = models.CharField(max_length=250, help_text="Comma separated, e.g. React, Vite, Bootstrap 5")
    badge = models.CharField(max_length=40, default="Web App", help_text="Web App / Mobile App / Full Stack ...")
    image = models.ImageField(upload_to="projects/", blank=True, help_text="Card image (landscape works best)")
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower number shows first")
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=120, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.project.title} - {self.caption or self.pk}"


class Skill(models.Model):
    CATEGORIES = [
        ("frontend", "Frontend Core"),
        ("backend", "Backend & DB"),
        ("ai", "AI (Learning)"),
        ("tools", "Tools & Workflow"),
        ("qa", "Testing & QA"),
    ]
    name = models.CharField(max_length=60)
    category = models.CharField(max_length=20, choices=CATEGORIES, default="frontend")
    icon = models.CharField(max_length=60, default="bi-code-slash", help_text="Bootstrap Icons class, e.g. bi-github")
    color = models.CharField(max_length=9, default="#38bdf8", help_text="Hex colour, e.g. #61dafb")
    order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name

class JourneyItem(models.Model):
    KINDS = [("experience", "Experience"), ("education", "Education")]
    kind = models.CharField(max_length=12, choices=KINDS, default="experience")
    title = models.CharField(max_length=150, help_text="Role (experience) or degree (education)")
    organization = models.CharField(max_length=200, help_text="Company or institution")
    period = models.CharField(max_length=60, help_text="e.g. Dec 2019 - Apr 2023")
    description = models.TextField()
    badge = models.CharField(max_length=60, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower number shows first")

    class Meta:
        ordering = ["kind", "order", "id"]

    def __str__(self):
        return f"{self.title} ({self.get_kind_display()})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.created_at:%d %b %Y}"
