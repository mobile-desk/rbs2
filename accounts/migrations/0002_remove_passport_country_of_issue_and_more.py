# Generated by Django 4.0.6 on 2025-02-05 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passport',
            name='country_of_issue',
        ),
        migrations.RemoveField(
            model_name='passport',
            name='expiry_date',
        ),
        migrations.RemoveField(
            model_name='passport',
            name='issue_date',
        ),
        migrations.RemoveField(
            model_name='passport',
            name='passport_number',
        ),
    ]
