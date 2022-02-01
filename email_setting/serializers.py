from rest_framework import serializers

from email_setting.models import EmailSetting

class EmailSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailSetting
        fields = "__all__"
        