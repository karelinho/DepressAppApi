from datetime import date
import datetime

from rest_framework import viewsets, status
from .models import Depress
from .serializers import DepressSerializer, UserSerializer
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.decorators import action

import pandas as pd

import smtplib, ssl
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders


class DepressViewSet(viewsets.ModelViewSet):
    queryset = Depress.objects.all()
    serializer_class = DepressSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['POST'])
    def send_message(self, request):
        try:
            port = 465
            password = "depressapp3902"  # input("Type your password and press enter: ")
            subject = "sledovani priznaku deprese"
            body = "Tento email byl vygenerovan automaticky. Prosim neodpovidejte na nej. V případě dotazu mne kontaktujte na adrese karel.sluka@gmail.com"
            sender_email = "depressapp@gmail.com"
            receiver_email = "karel.sluka@gmail.com"
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            # message["Bcc"] = "karel.sluka@gmail.com"
            filename = "karelsluka.xlsx"
            message.attach(MIMEText(body, "plain"))

            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)

            part.add_header(
                "Content-Disposition",
                f"attachment; filename=  {filename}",
            )

            message.attach(part)
            text = message.as_string()

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login("depressapp@gmail.com", password)
                server.sendmail(sender_email, receiver_email, text)

            response = {'message': 'an email was sent'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'failed to send email'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Depress.objects.all()
        date_data = self.request.query_params['date']
        dateTo = date.fromisoformat(date_data)
        dateFrom = dateTo - datetime.timedelta(days=7)
        return queryset.filter(date__range=[dateFrom, dateTo])

    @action(detail=True, methods=['POST'])
    def send_depress(self, request, pk=None):
        if 'date' in request.data:
            new_date = request.data['date']
            sleep = request.data['sleep']
            headache = request.data['headache']
            tiredness = request.data['tiredness']
            appetite = request.data['appetite']
            constipation = request.data['constipation']
            self_blame_thoughts = request.data['self_blame_thoughts']
            mood = request.data['mood']
            self_destructive_thoughts = request.data['self_destructive_thoughts']
            concentration = request.data['concentration']
            physical_discomfort = request.data['physical_discomfort']
            tense_feeling = request.data['tense_feeling']
            sleep_length = request.data['sleep_length']
            user = request.user
            # user = User.objects.get(id=1)

            pyxl_df = pd.read_excel('karelsluka.xlsx', sheet_name=0, engine='openpyxl', dtype={'datum': date})
            writer = pd.ExcelWriter('karelsluka.xlsx', engine='xlsxwriter', date_format='DD.MM.YYYY',
                                    datetime_format='DD.M.YY')
            book = writer.book
            header_format = book.add_format({
                'text_wrap': True,
                'rotation': 90
            })
            parsed_date = new_date.split('-')
            df = pd.DataFrame({
                'datum': [datetime.datetime(int(parsed_date[0]), int(parsed_date[1]), int(parsed_date[2]))],
                'spánek': [sleep],
                'bolest hlavy': [headache],
                'únava': [tiredness],
                'chuť k jídlu': [appetite],
                'zácpa': [constipation],
                'sebeobviňující myšlenky': [self_blame_thoughts],
                'nálada': [mood],
                'sebedestruktivní myšlenky': [self_destructive_thoughts],
                'soustředěnost': [concentration],
                'tělesná nepohoda': [physical_discomfort],
                'pocit napětí': [tense_feeling],
                'délka spánku + odpočinku': [sleep_length]
            })
            df = df.append(pyxl_df)
            pd.to_datetime(df['datum'])
            df.to_excel(writer, sheet_name='New', startrow=0, index=False, freeze_panes=(1, 0))
            worksheet = writer.sheets.setdefault('New')
            for col_num, value in enumerate(df.columns.values):
                worksheet.set_row(0, 150)
                worksheet.write(0, col_num, value, header_format)
            writer.save()

            try:
                depress_data = Depress.objects.get(user=user.id, date=new_date)
                depress_data.date = new_date
                depress_data.sleep = sleep
                depress_data.headache = headache
                depress_data.tiredness = tiredness
                depress_data.appetite = appetite
                depress_data.constipation = constipation
                depress_data.self_blame_thoughts = self_blame_thoughts
                depress_data.mood = mood
                depress_data.self_destructive_thoughts = self_destructive_thoughts
                depress_data.concentration = concentration
                depress_data.physical_discomfort = physical_discomfort
                depress_data.tense_feeling = tense_feeling
                depress_data.sleep_length = sleep_length
                depress_data.save()
                serializer = DepressSerializer(depress_data, many=False)
                # self.export_to_excel(depress_data);
                response = {'message': 'Depress updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                depress_object = Depress.objects.create(user=user, date=new_date, sleep=sleep, headache=headache,
                                                tiredness=tiredness, appetite=appetite, constipation=constipation,
                                                self_blame_thoughts=self_blame_thoughts, mood=mood,
                                                self_destructive_thoughts=self_destructive_thoughts,
                                                concentration=concentration, physical_discomfort=physical_discomfort,
                                                tense_feeling=tense_feeling, sleep_length=sleep_length)
                serializer = DepressSerializer(depress_object, many=False)
                response = {'message': 'Depress created', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'you need to provide depress data'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
