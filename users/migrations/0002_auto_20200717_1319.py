# Generated by Django 2.2.5 on 2020-07-17 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='icon',
            field=models.ImageField(default='icons/default.png', upload_to='icons/', verbose_name='アイコン'),
        ),
    ]
