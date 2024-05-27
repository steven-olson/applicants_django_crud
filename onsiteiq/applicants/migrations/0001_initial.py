# Generated by Django 5.0.6 on 2024-05-27 04:34

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('first_name', models.CharField(editable=False, max_length=30)),
                ('last_name', models.CharField(editable=False, max_length=30)),
                ('email_address', models.CharField(editable=False, max_length=500)),
                ('phone_number', models.CharField(editable=False, max_length=20)),
                ('note', models.CharField(blank=True, max_length=500, null=True)),
                ('approval_status', models.BooleanField(default=False)),
            ],
            options={
                'permissions': [('can_view_applicant', 'Can view existing applicants'), ('can_create_applicant', 'Can create new applicants'), ('can_accept_reject_applicant', 'Can edit `approval_status` field on an applicant'), ('can_create_update_note', 'Can update `note` field on an applicant')],
            },
        ),
    ]