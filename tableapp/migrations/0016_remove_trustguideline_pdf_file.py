# Generated by Django 5.0.4 on 2025-01-17 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tableapp', '0015_trustguideline_pdf_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trustguideline',
            name='pdf_file',
        ),
    ]
