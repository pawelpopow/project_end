# Generated by Django 4.0.4 on 2022-04-12 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_day', models.DateField()),
                ('end_day', models.DateField()),
                ('amount_people', models.PositiveSmallIntegerField()),
                ('booked_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=20)),
                ('profile_pic', models.ImageField(blank=True, upload_to='image')),
                ('phone_number', models.CharField(max_length=50)),
                ('address', models.TextField()),
                ('state', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_yacht', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, default=2000.0, max_digits=7)),
                ('is_available', models.BooleanField(default=True)),
                ('yacht_image', models.ImageField(default='0.jpeg', upload_to='yacht')),
            ],
        ),
    ]