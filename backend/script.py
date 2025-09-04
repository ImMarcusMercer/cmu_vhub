from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()
u = User.objects.get(username="Janmarc")

# Assign a role
u.groups.add(Group.objects.get(name="staff"))

# Remove a role
# u.groups.remove(Group.objects.get(name="student"))

# See roles
# list(u.groups.values_list("name", flat=True))