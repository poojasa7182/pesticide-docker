# Generated by Django 3.1.1 on 2022-01-30 18:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pesticide_app', '0015_auto_20220131_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webhookdetails',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='webhook_creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
