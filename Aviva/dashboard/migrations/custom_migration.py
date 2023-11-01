from django.contrib.auth.hashers import make_password
from dashboard.models import AllUsers, CustomUser
from django.db import migrations


def migrate_user_data(apps, schema_editor):
    for all_user in AllUsers.objects.all():
        custom_user = CustomUser(
            email=all_user.email,
            fullname=all_user.fullname,
            phone=all_user.phone,
            state=all_user.state,
            facility=all_user.facility,
            usercategory=all_user.usercategory,
        )
        custom_user.password = make_password(all_user.password)  # Update password hashing
        custom_user.save()

def reverse_migration(apps, schema_editor):
    CustomUser.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_customuser'),  # Replace 'yourapp' and 'previous_migration'
    ]

    operations = [
        migrations.RunPython(migrate_user_data, reverse_migration),
    ]
