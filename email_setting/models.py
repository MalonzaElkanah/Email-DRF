from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

# Create your models here.

class EmailSetting(AbstractBaseUser):
	name = models.CharField('Name', max_length=50)
	email = models.CharField('Email', max_length=50, unique=True)
	smtp_server = models.CharField('SMTP SERVER', max_length=100)
	smtp_port = models.IntegerField('SMTP Port', default=587)
	imap_server = models.CharField('IMAP SERVER', max_length=100, default="imap.gmail.com")
	imap_port = models.IntegerField('IMAP Port', default=993)
	# name, email, password, smtp_server, smtp_port, imap_server, imap_port

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["username"]

	def __str__(self):
		return self.email

	class Meta:
		ordering = ('id',)

