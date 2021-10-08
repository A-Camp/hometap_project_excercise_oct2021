# Generated by Django 3.1.13 on 2021-10-08 01:37

from django.db import migrations, models
import django.db.models.deletion
import localflavor.us.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(max_length=100)),
                ('zipcode', localflavor.us.models.USZipCodeField(max_length=10)),
                ('city', models.CharField(max_length=60)),
                ('state', localflavor.us.models.USStateField(max_length=2)),
                ('has_septic', models.BooleanField(null=True)),
                ('user_sewer_info', models.CharField(max_length=1000)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='septic_api.user')),
            ],
        ),
    ]