# Generated by Django 5.1.4 on 2024-12-21 08:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_vehicle_status_component_vehicle'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='total_cost',
            new_name='cost',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='vehicle',
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Completed'), (2, 'Pending'), (3, 'On Hold')], default=3)),
                ('issue_description', models.CharField(blank=True, max_length=250, null=True)),
                ('registration_number', models.CharField(max_length=255, unique=True)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(1, 'Paid'), (2, 'Not Paid'), (3, 'On Hold')], default=3)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.service')),
            ],
        ),
        migrations.AddField(
            model_name='issue',
            name='service',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='main.service'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
