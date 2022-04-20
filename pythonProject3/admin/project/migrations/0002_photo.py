# Generated by Django 3.2.12 on 2022-02-01 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_url', models.ImageField(upload_to='images')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo', to='project.product')),
            ],
        ),
    ]