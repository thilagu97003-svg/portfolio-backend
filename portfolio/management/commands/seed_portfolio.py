"""
Fills the database with the content that used to be hard-coded in the React app.
Safe to run more than once (it updates instead of duplicating).

    python manage.py seed_portfolio --assets "..\\my-portfolio\\src\\assets"

--assets is optional: it copies the project card images (grocery.png, task-master.png ...) into Django.
--only profile|projects|skills|journey runs just one part (handy to add new skills without touching the rest).
Existing records are NEVER overwritten, so your admin edits are safe.
"""
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from portfolio.models import JourneyItem, Project, Skill, SiteProfile, Stat

PROFILE = dict(
    display_name="Thilaga",
    full_name="K. Thilagavathi",
    initials="KT",
    role="Full Stack Developer",
    tagline="Crafting responsive, pixel-perfect web apps with React and Bootstrap, and powering them with Django and REST APIs.",
    bio="Full Stack Developer with 4+ years of professional experience, building responsive, pixel-perfect web apps with React, JavaScript, and Bootstrap, and backends with Python, Django, and REST APIs.",
    email="thilagu97003@gmail.com",
    github_url="https://github.com/thilagu97003-svg",
    linkedin_url="https://www.linkedin.com/in/k-thilagavathi-325401427/",
    location="Tamil Nadu, India",
    work_mode="Open for 100% Remote / Work From Home (Full-Time)",
    available_for_hire=True,
)
STATS = [("8+", "Live Apps"), ("4+ Yrs", "Experience"), ("Full Stack", "React + Django")]

# (title, badge, tech_stack, live, github, image file, description, features)
PROJECTS = [
    ("FoodFlow Delivery App", "Mobile App", "React Native, Expo, TypeScript, Expo Router, Firebase Auth",
     "https://foodflowapp-flame.vercel.app/", "https://github.com/thilagu97003-svg/FoodFlowApp", "foodflow.png",
     "Food delivery mobile app with onboarding, email login and sign up, restaurant search, category browsing, popular items, cart with quantity controls, order tracking and a profile screen. Built with Expo and React Native, with Firebase authentication, and deployed as a web app on Vercel.",
     "Animated splash screen and 3-slide onboarding\nLogin and Sign up with show/hide password and Forgot Password\nHome with delivery address, restaurant search, offer banner, categories and popular items\nCart with quantity controls, item badge on the tab and total price\nOrders screen with Active and Past tabs, delivery status, ETA and Track option\nProfile with order history, addresses and payments tabs\nResponsive web build deployed on Vercel"),
    ("Photography Portfolio", "Website", "HTML5, CSS3, JavaScript, Responsive UI",
     "https://photography-portfolio-eight-henna.vercel.app/", "https://github.com/thilagu97003-svg/PhotographyPortfolio", "photography.png",
     "Multi-page visual showcase featuring curated photo galleries, fluid layouts, pricing plans, and smooth user interactions.",
     "Grid layout photo galleries\nImage lightbox\nPricing plans\nMobile-first responsive design"),
    ("Grocery E-Commerce Platform", "Web App", "React, Vite, JavaScript, Bootstrap 5, CSS3",
     "https://groceryshop-wheat.vercel.app/", "https://github.com/thilagu97003-svg/Groceryshop", "grocery.png",
     "Full-featured shopping web app with catalog search, product filters, cart management, and a responsive checkout experience.",
     "Home, About Us, Categories and Contact pages\nCategory-wise product browsing\nSearch, cart and wishlist icons\nContact form"),
    ("Charity & NGO Foundation Website", "Web App", "React, Vite, JavaScript, Bootstrap 5, CSS3",
     "https://charityproject-sandy.vercel.app/", "https://github.com/thilagu97003-svg/CharityProject", "charity.png",
     "Responsive charity portal highlighting community missions, cause campaigns, donation flows, and volunteer engagement.",
     "Home, About Us, Causes, Volunteer and Contact pages\nHero section with Donate Now and Become a Volunteer actions\nFully responsive layout"),
    ("TaskMaster App", "Mobile App", "React Native, Expo, JavaScript, AsyncStorage",
     "https://task-masterapp.vercel.app/", "https://github.com/thilagu97003-svg/TodoListApp", "task-master.png",
     "Task management app to organize your day. Add tasks with category, due date, time and subtasks, search and filter by category, track overall progress, and move finished tasks to a Completed list. Overdue tasks are highlighted automatically.",
     "Add tasks with category, due date, time and subtasks\nSearch and category filters\nOverall progress bar\nCategories tab with per-category progress\nCompleted tab with Clear History\nOverdue badge on late tasks"),
    ("AI Compass", "Mobile App", "React Native, Expo, React Navigation, AsyncStorage",
     "https://ai-compass-nine-alpha.vercel.app/", "https://github.com/thilagu97003-svg/AI-Compass", "ai-compass.png",
     "Learning app that teaches beginners how to use AI tools step by step. Covers 8 AI tools with guides, ready-to-copy prompts and quizzes, a Find My Tool workflow suggester, and an AI Dictionary in English and Tamil. Progress and quiz scores are saved on the device.",
     "8 AI tools with speciality, advantages, disadvantages and limitations\nStep-by-step guide and ready-to-copy prompts for every tool\nFind My Tool: describe a project and get a tool workflow\n5-question quiz for every tool\nAI Dictionary in English and Tamil\nProgress tracking saved on the device"),
    ("Supplyhive Stationery Store", "Full Stack", "Django, Python, HTML5, CSS3, JavaScript",
     "https://stationarywebsite.vercel.app/", "https://github.com/thilagu97003-svg/stationarywebsite", "stationery.png",
     "Multi-page stationery e-commerce website built with Django from a Figma design. Includes category-wise shopping with price filters, product ratings, bulk-order pricing, add to cart, search, a contact page with embedded map, and a registration form with live password validation.",
     "Five shop categories with price filter\nProduct ratings and bulk-order pricing\nAdd to cart and search\nContact page with embedded map\nCreate Account form with live password checklist"),
    ("StepUp.in Shoe Store", "Full Stack", "React, Django, REST API, PostgreSQL, Cloudinary",
     "https://shoe-store-frontend-rouge.vercel.app/", "https://github.com/thilagu97003-svg/Ecommerce-backend", "shoe-store.png",
     "Full-stack shoe e-commerce website built from a Figma design. Features a promotional banner slider, category navigation (Womens, Mens, Kids, Brands, Offers), a New & Trending product listing fetched from a Django REST API, login and register with password toggle, cart counter, and an enquiry form. Frontend on Vercel, backend with PostgreSQL on Render.",
     "Promotional banner slider\nWomens, Mens, Kids, Brands and Offers navigation\nNew & Trending products from a Django REST API\nLogin and Register with show/hide password\nCart counter and enquiry form"),
]

# (name, category, icon, colour)
SKILLS = [
    ("React.js", "frontend", "bi-filetype-jsx", "#61dafb"),
    ("JavaScript", "frontend", "bi-filetype-js", "#f7df1e"),
    ("HTML5", "frontend", "bi-filetype-html", "#e34f26"),
    ("CSS3", "frontend", "bi-filetype-css", "#1572b6"),
    ("Bootstrap 5", "frontend", "bi-bootstrap-fill", "#7952b3"),
    ("Responsive UI", "frontend", "bi-phone", "#38bdf8"),
    ("Python", "backend", "bi-filetype-py", "#3776ab"),
    ("Django", "backend", "bi-hdd-rack-fill", "#44b78b"),
    ("REST APIs", "backend", "bi-diagram-3-fill", "#f97316"),
    ("MySQL", "backend", "bi-database-fill", "#00758f"),
    ("MongoDB", "backend", "bi-database-fill-gear", "#47a248"),
    ("PostgreSQL", "backend", "bi-database-fill-check", "#336791"),
    ("Generative AI", "ai", "bi-stars", "#f59e0b"),
    ("LLMs & Prompting", "ai", "bi-chat-square-text-fill", "#a78bfa"),
    ("LangChain", "ai", "bi-link-45deg", "#22c55e"),
    ("LangGraph", "ai", "bi-diagram-2-fill", "#38bdf8"),
    ("AI Agents", "ai", "bi-robot", "#f43f5e"),
    ("Vector Databases", "ai", "bi-boxes", "#06b6d4"),
    ("ML Basics", "ai", "bi-graph-up-arrow", "#f97316"),
    ("Git & GitHub", "tools", "bi-github", "#f05032"),
    ("VS Code", "tools", "bi-laptop", "#007acc"),
    ("Figma to Code", "tools", "bi-bounding-box-circles", "#a259ff"),
    ("Vercel", "tools", "bi-cloud-arrow-up-fill", "#ffffff"),
    ("QA Testing", "qa", "bi-patch-check-fill", "#22c55e"),
    ("Cross-Browser", "qa", "bi-browser-chrome", "#3b82f6"),
]

# (kind, title, organization, period, description, badge)
JOURNEY = [
    ("experience", "Full Stack Developer (Trainee / Course)", "Vetri Technology Solutions, Tenkasi", "July 2026 - Present",
     "Building full-stack web applications and GenAI implementations. Engineering interactive frontends with React.js, modern CSS, and Python backend fundamentals.", "Current"),
    ("experience", "Lecturer / Academic Instructor", "P.A.C. Ramasamy Raja Polytechnic College, Rajapalayam", "Dec 2019 - Apr 2023",
     "Taught technical curriculum, guided student engineering projects, and managed lab sessions with a focus on clear technical communication and structured problem-solving.", "Academic / 3.4 Yrs"),
    ("experience", "Quality Assurance Investigator (QAI)", "Jay Jay Mills India Pvt Ltd, Perundurai, Erode", "Apr 2019 - Nov 2019",
     "Conducted systematic quality investigations, process audits, and root-cause analysis across production workflows.", "Quality Assurance"),
    ("experience", "Quality Assurance Investigator (QAI)", "Sri Saravana Spinning Mills Ltd, Dindigul", "May 2015 - Jun 2016",
     "Managed rigorous quality investigation protocols, defect identification, and operational compliance reporting.", "Quality Assurance"),
    ("education", "B.Tech in Textile Technology", "Bannari Amman Institute of Technology, Erode", "2016 - 2019",
     "Cultivated strong analytical reasoning, mathematical fundamentals, and process optimization techniques.", "Bachelor's Degree"),
    ("education", "Diploma in Textile Technology", "P.A.C. Ramasamy Raja Polytechnic College, Rajapalayam", "2012 - 2015",
     "Built a strong technical base in process mechanics and laboratory operations (later returned to serve as faculty).", "Diploma"),
]


class Command(BaseCommand):
    help = "Load the portfolio content that used to live inside the React files."

    def add_arguments(self, parser):
        parser.add_argument("--assets", help="Folder with project images (React src/assets)")
        parser.add_argument("--only", choices=["profile", "projects", "skills", "journey"],
                            help="Load just one part")

    def handle(self, *args, **opts):
        only = opts.get("only")
        run = lambda part: only in (None, part)

        if run("profile"):
            profile, _ = SiteProfile.objects.get_or_create(pk=1, defaults=PROFILE)
            if not profile.stats.exists():
                for i, (value, label) in enumerate(STATS):
                    Stat.objects.create(profile=profile, value=value, label=label, order=i)

        if run("projects"):
            assets = Path(opts["assets"]) if opts.get("assets") else None
            for i, (title, badge, tech, live, gh, img, desc, feats) in enumerate(PROJECTS, start=1):
                project, _ = Project.objects.get_or_create(
                    title=title,
                    defaults=dict(badge=badge, tech_stack=tech, live_url=live, github_url=gh,
                                  description=desc, features=feats, order=i, is_published=True),
                )
                src = assets / img if assets else None
                if src and src.exists() and not project.image:
                    with open(src, "rb") as fh:
                        project.image.save(img, File(fh), save=True)
                elif assets and not (src and src.exists()):
                    self.stdout.write(self.style.WARNING(f"  image not found: {img}"))

        if run("skills"):
            for i, (name, cat, icon, color) in enumerate(SKILLS, start=1):
                Skill.objects.get_or_create(name=name, defaults=dict(category=cat, icon=icon, color=color, order=i))

        if run("journey"):
            for i, (kind, title, org, period, desc, badge) in enumerate(JOURNEY, start=1):
                JourneyItem.objects.get_or_create(
                    kind=kind, title=title, organization=org,
                    defaults=dict(period=period, description=desc, badge=badge, order=i),
                )
        self.stdout.write(self.style.SUCCESS("Portfolio data loaded (existing records were left untouched)."))
