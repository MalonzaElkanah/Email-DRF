from django.http import HttpResponse

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from email_setting.models import EmailSetting
from email_setting.serializers import EmailSettingsSerializer, ComposeEmailSerializer

from . import mail_lib


class EmailSettingListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EmailSettingsSerializer
    queryset = EmailSetting.objects.all()

class EmailSettingUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmailSettingsSerializer
    queryset = EmailSetting.objects.all()


@api_view(['GET'])
def test_settings(request, pk):
    settings = EmailSetting.objects.filter(id=pk)
    if settings.count() > 0:
        connection = mail_lib.check_connection(settings[0]) 
        if connection:
            return Response({'results': {'connection': 'success'}}, status=status.HTTP_200_OK)
        else:
            return Response({'results': {'connection': connection,}}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def inbox_apiview(request, pk):
    settings = EmailSetting.objects.filter(id=pk)
    if settings.count() > 0:
        subjects = mail_lib.get_email_subjects("INBOX", 1, settings[0])
        mail_labels = mail_lib.email_labels(settings[0])
        items = {'results':{'emails': subjects, 'labels': mail_labels}}
        return Response(items, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def label_mails(request, pk, label):
    settings = EmailSetting.objects.filter(id=pk)
    if settings.count() > 0:
        label = '"'+label.replace('-', ' ').title()+'"'
        subjects = mail_lib.get_email_subjects(label, 1, settings[0])
        mail_labels = mail_lib.email_labels(settings[0])
        items = {'results':{'emails': subjects, 'labels': mail_labels}}
        return Response(items, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def read_email(request, pk, label, email_id):
    settings = EmailSetting.objects.filter(id=pk)
    if settings.count() > 0:
        label = '"'+label.replace('-', ' ').title()+'"'
        email = mail_lib.get_email(int(email_id), label, settings[0])
        mail_labels = mail_lib.email_labels(settings[0])
        items = {'results':{'email': email, 'labels': mail_labels}}
        return Response(items, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_attachment(request, pk, label, email_id, attachment_id):
    settings = EmailSetting.objects.filter(id=pk)
    if settings.count() > 0:
        email = mail_lib.get_email(int(email_id), label, settings[0])
        attachments = []
        if email["is_attachment"]:
            files = email["attachments"]
            attachment_id = int(attachment_id)
            count = 1
            for name, filepath in files.items():
                if count == attachment_id:
                    file = open(filepath, 'rb')
                    response = HttpResponse(file, content_type='application/octet-stream')
                    response['Content-Disposition'] = 'inline; filename="' + name + '"'
                    return response
                count += 1
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def compose_email(request, pk):
    settings = EmailSetting.objects.filter(id=pk)
    if settings.count() > 0:
        reciever_email = request.POST['email']
        subject = request.POST['subject']
        content = request.POST['content']
        email_data = {"subject": subject, "content": content, "email": reciever_email, 
            "attachments": request.FILES.getlist("attachments")}
        email = mail_lib.send_email(email_data, settings[0])
        return Response(email, status=status.HTTP_200_OK)  
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)  


class ComposeEmailAPIView(generics.CreateAPIView):
    serializer_class = ComposeEmailSerializer

    """  Send a new Email.  """
    def perform_create(self, serializer, *args, **kwargs):
        settings = EmailSetting.objects.filter(id=self.kwargs['pk'])
        if settings.count() > 0:
            # serializer = ComposeEmailSerializer(data=request.data)
            if serializer.is_valid():
                email = mail_lib.send_email(serializer.initial_data, settings[0])
                return Response(email, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
