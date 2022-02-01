# Generated by Django 3.1.4 on 2022-02-01 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('email', models.CharField(max_length=50, verbose_name='Email')),
                ('password', models.CharField(max_length=1000, verbose_name='Password')),
                ('smtp_server', models.CharField(max_length=100, verbose_name='SMTP SERVER')),
                ('smtp_port', models.IntegerField(default=587, verbose_name='Port')),
                ('imap_server', models.CharField(default='imap.gmail.com', max_length=100, verbose_name='SMTP SERVER')),
                ('imap_port', models.IntegerField(default=993, verbose_name='Port')),
            ],
        ),
    ]