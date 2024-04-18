# Generated by Django 5.0.4 on 2024-04-18 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guideline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('external_url', models.URLField(blank=True, max_length=255, null=True)),
                ('metadata', models.TextField(default='General')),
                ('medical_speciality', models.CharField(default='General', max_length=255)),
            ],
        ),
    ]
