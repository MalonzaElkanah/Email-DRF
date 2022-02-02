from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.

class EmailSetting(AbstractUser):
	name = models.CharField('Name', max_length=50)
	email = models.CharField('Email', max_length=50, unique=True)
	# password = models.CharField('Password', max_length=1000)
	smtp_server = models.CharField('SMTP SERVER', max_length=100)
	smtp_port = models.IntegerField('SMTP Port', default=587)
	imap_server = models.CharField('IMAP SERVER', max_length=100, default="imap.gmail.com")
	imap_port = models.IntegerField('IMAP Port', default=993)
	# name, email, password, smtp_server, smtp_port, imap_server, imap_port

	objects = UserManager()

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["name"]

	def __str__(self):
		return self.email

	class Meta:
		ordering = ('id',)

