from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from email_setting.models import EmailSetting
from email_setting.serializers import EmailSettingsSerializer

from . import mail_lib


class EmailSettingListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EmailSettingsSerializer
    queryset = EmailSetting.objects.all()

class EmailSettingUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmailSettingsSerializer
    queryset = EmailSetting.objects.all()


@api_view(['GET'])
def test_settings(request, pk):
    pass 


@api_view(['GET'])
def inbox_apiview(request, pk):
    settings = EmailSetting.objects.filter(id=pk)
    if settings.count() > 0:
        subjects = mail_lib.get_email_subjects("INBOX", 1, settings[0])
        mail_labels = mail_lib.email_labels(settings[0])

        items = {
            'results': 
                {
                    'emails': subjects, 
                    'labels': mail_labels
                }
        }

        return Response(items, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def label_mails(request, pk):
        pass


@api_view(['GET'])
def read_email(request, slug, email_id, category):
    pass


@api_view(['GET'])
def get_attachment(request, pk, category, attachment_id):
    pass 


@api_view(['POST'])
def compose_email(request):
    pass
