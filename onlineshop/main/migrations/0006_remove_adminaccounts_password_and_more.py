# Generated by Django 4.2.4 on 2023-08-30 13:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_adminaccounts_offeredproduct_featuredproduct_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminaccounts',
            name='password',
        ),
        migrations.AddField(
            model_name='adminaccounts',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='adminaccounts',
            name='first_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='adminaccounts',
            name='last_name',
            field=models.CharField(default=12, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='adminaccounts',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
