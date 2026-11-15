# Portfolio backend (Django + DRF)

Local setup (Windows, run inside this folder):

    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py seed_portfolio --assets "..\my-portfolio\src\assets"
    python manage.py runserver

Admin: http://127.0.0.1:8000/admin/     API: http://127.0.0.1:8000/api/projects/
Endpoints: /api/profile/  /api/projects/  /api/skills/  /api/journey/  POST /api/contact/
Production settings come from environment variables: see .env.example
