# Generated by Django 5.1.2 on 2024-10-09 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='status',
            field=models.IntegerField(choices=[(1, 'Completed'), (2, 'Pending'), (3, 'On Hold')], default=True),
        ),
    ]
