# Generated by Django 3.2.6 on 2021-10-25 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Blog', '0002_alter_article_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='great',
            name='userIp',
            field=models.GenericIPAddressField(null=True, verbose_name='IP'),
        ),
    ]