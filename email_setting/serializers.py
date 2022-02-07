from rest_framework import serializers

from email_setting.models import EmailSetting
from django.contrib.auth import get_user_model

class EmailSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailSetting
        fields = '__all__' # [ "email", "password", "name", "smtp_server", "smtp_port", "imap_server", "imap_port"]
        