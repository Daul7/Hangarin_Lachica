import os
import django
import random
from faker import Faker
from django.contrib.auth.models import User
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hangarin_Lachica.settings')
django.setup()

from hangarinapp.models import Task, SubTask, Note, Priority, Category

fake = Faker()

# ----- 1. Create or update superuser -----
SUPERUSER_USERNAME = "admin"
SUPERUSER_EMAIL = "admin@example.com"
SUPERUSER_PASSWORD = "admin123"

if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
    print("Creating superuser...")
    User.objects.create_superuser(SUPERUSER_USERNAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD)
else:
    print("Superuser already exists. Updating password...")
    user = User.objects.get(username=SUPERUSER_USERNAME)
    user.set_password(SUPERUSER_PASSWORD)
    user.save()

# ----- 2. Add Priority records -----
priority_names = ["High", "Medium", "Low", "Critical", "Optional"]
for name in priority_names:
    Priority.objects.get_or_create(name=name)
print("Priorities added.")

# ----- 3. Add Category records -----
category_names = ["Work", "School", "Personal", "Finance", "Projects"]
for name in category_names:
    Category.objects.get_or_create(name=name)
print("Categories added.")

# ----- 4. Populate Tasks, SubTasks, Notes -----
priorities = list(Priority.objects.all())
categories = list(Category.objects.all())

for _ in range(10):  # 10 Tasks
    task = Task.objects.create(
        title=fake.sentence(nb_words=5),
        description=fake.paragraph(nb_sentences=3),
        status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
        deadline=timezone.make_aware(fake.date_time_this_month()),
        priority=random.choice(priorities),
        category=random.choice(categories),
    )

    # SubTasks
    for _ in range(random.randint(1, 3)):
        SubTask.objects.create(
            task=task,
            title=fake.sentence(nb_words=5),
            status=fake.random_element(elements=["Pending", "In Progress", "Completed"])
        )

    # Notes
    for _ in range(random.randint(1, 2)):
        Note.objects.create(
            task=task,
            content=fake.paragraph(nb_sentences=2)
        )

print("Tasks, SubTasks, and Notes populated successfully!")
