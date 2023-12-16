# Generated by Django 4.2.7 on 2023-12-16 21:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("chat", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="users",
            field=models.ManyToManyField(
                blank=True, related_name="rooms", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="invitation",
            name="invitor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="invitation",
            name="room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="invitations",
                to="chat.room",
            ),
        ),
    ]
