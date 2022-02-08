from rest_framework import serializers

from email_setting.models import EmailSetting
from django.contrib.auth import get_user_model

class EmailSettingsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = EmailSetting
        fields = '__all__' 
        # [ "email", "password", "name", "smtp_server", "smtp_port", "imap_server", "imap_port"]


class ComposeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=70)
    content = serializers.CharField(
        max_length=200, 
        style={'base_template': 'textarea.html','rows':5}
    )
    # attachments = serializers.FileField(allow_empty_file=True, required=False)
    attachments = serializers.ListField(
        child=serializers.FileField(allow_empty_file=True, required=False), 
        allow_empty=True,
        required=False 
    )