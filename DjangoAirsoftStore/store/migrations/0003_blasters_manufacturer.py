# Generated by Django 4.1.4 on 2022-12-17 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_gear'),
    ]

    operations = [
        migrations.AddField(
            model_name='blasters',
            name='manufacturer',
            field=models.CharField(default='Vendor', max_length=255),
            preserve_default=False,
        ),
    ]
