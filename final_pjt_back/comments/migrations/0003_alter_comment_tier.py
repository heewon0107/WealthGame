# Generated by Django 4.2.11 on 2024-11-25 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_comment_tier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='tier',
            field=models.CharField(max_length=20),
        ),
    ]