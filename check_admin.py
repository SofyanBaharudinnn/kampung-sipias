import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from django.contrib.auth.models import User

users = User.objects.all()
print("TOTAL USERS:", users.count())
for u in users:
    print(f"User: {u.username}, Superuser: {u.is_superuser}, Active: {u.is_active}")

if not users.exists():
    User.objects.create_superuser('admin', 'admin@sipias.id', 'admin123')
    print("CREATED DEFAULT SUPERUSER -> username: admin | password: admin123")
else:
    u = users.first()
    u.set_password('admin123')
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print(f"UPDATED USER '{u.username}' PASSWORD TO: admin123")
