from django.db import models

# Create your models here.

class EmailSetting(models.Model):
	name = models.CharField('Name', max_length=50)
	email = models.CharField('Email', max_length=50)
	password = models.CharField('Password', max_length=1000)
	smtp_server = models.CharField('SMTP SERVER', max_length=100)
	smtp_port = models.IntegerField('SMTP Port', default=587)
	imap_server = models.CharField('IMAP SERVER', max_length=100, default="imap.gmail.com")
	imap_port = models.IntegerField('IMAP Port', default=993)
	# name, email, password, smtp_server, smtp_port, imap_server, imap_port

