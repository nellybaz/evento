# Generated by Django 2.2.6 on 2019-10-19 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automate_pdf', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='invite_file',
            field=models.FileField(upload_to='invite_files'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='invitees',
            field=models.FileField(upload_to='invitees'),
        ),
    ]
