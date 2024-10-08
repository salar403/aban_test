# Generated by Django 4.0.8 on 2024-08-21 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Portfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=20, default=0, max_digits=40)),
                ('blocked', models.DecimalField(decimal_places=20, default=0, max_digits=40)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_balance', models.DecimalField(decimal_places=20, max_digits=40)),
                ('balance_change', models.DecimalField(decimal_places=20, max_digits=40)),
                ('end_balance', models.DecimalField(decimal_places=20, max_digits=40)),
                ('start_blocked', models.DecimalField(decimal_places=20, max_digits=40)),
                ('blocked_change', models.DecimalField(decimal_places=20, max_digits=40)),
                ('end_blocked', models.DecimalField(decimal_places=20, max_digits=40)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=100)),
                ('portfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='accounting.portfo')),
            ],
        ),
    ]
