# Generated by Django 2.2.5 on 2020-07-21 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200717_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='icon',
            field=models.ImageField(default='icon/default.png', upload_to='icons/', verbose_name='アイコン'),
        ),
    ]
