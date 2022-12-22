# Generated by Django 4.0.4 on 2022-12-20 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='banner/image-%y-%m-%d/', verbose_name='Banner rasmi')),
                ('title', models.CharField(max_length=255, verbose_name='Sarlavha')),
                ('description', models.TextField(verbose_name='Malumot')),
                ('to_url', models.URLField(verbose_name='Manzil')),
            ],
        ),
    ]