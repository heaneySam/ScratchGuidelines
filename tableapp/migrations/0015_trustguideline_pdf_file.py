# Generated by Django 5.0.4 on 2025-01-03 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tableapp', '0014_alter_trustguideline_authors_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trustguideline',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='pdfs/'),
        ),
    ]
