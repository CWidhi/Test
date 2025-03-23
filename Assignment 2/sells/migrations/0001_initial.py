# Generated by Django 3.2.25 on 2025-03-23 06:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('items', '0003_auto_20250323_0022'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellHeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SellDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('header_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='sells.sellheader')),
                ('item_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.items')),
            ],
        ),
    ]
