from rest_framework import generics

from email_setting.models import EmailSetting
from email_setting.serializers import EmailSettingsSerializer


class EmailSettingListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EmailSettingsSerializer
    queryset = EmailSetting.objects.all()

class EmailSettingUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmailSettingsSerializer
    queryset = EmailSetting.objects.all()