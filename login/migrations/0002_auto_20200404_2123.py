# Generated by Django 3.0.4 on 2020-04-04 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='c_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='注册时间'),
        ),
    ]