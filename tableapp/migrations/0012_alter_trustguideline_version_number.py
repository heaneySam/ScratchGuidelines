# Generated by Django 5.0.4 on 2024-05-18 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tableapp', '0011_trustguideline_authors_trustguideline_creation_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trustguideline',
            name='version_number',
            field=models.CharField(default='0', max_length=50),
        ),
    ]
