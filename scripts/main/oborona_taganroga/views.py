from email import message
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.mixins import *
from rest_framework import generics, status
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView, exception_handler
from rest_framework.exceptions import APIException 
from rest_framework.validators import UniqueValidator
# from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import bad_request
from django.db.models import Prefetch
from django.contrib.auth.tokens import default_token_generator
import phonenumbers
import datetime
from django.template import Context
from django.template.loader import get_template

# Для загрузки файлов
import mimetypes
import os
from django.http.response import HttpResponse
import xlsxwriter
from .forms import *
from django.http import HttpResponseRedirect

class ParticipantCreate(APIView):
    # permission_classes = [AllowAny]
    #API that allows to create new Participant
    def post(self, request):
        participantizer = ParticipantCreateSerializer(data=request.data)
        if participantizer.is_valid(raise_exception=True):
            print(participantizer.data['phonenumber'])
            if participantizer.data['phonenumber'] != '':
                parsedPhone = phonenumbers.parse(participantizer.data['phonenumber'], "RU")
                if not phonenumbers.is_possible_number(parsedPhone):
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            participant = Participant.objects.create(phonenumber = participantizer.data['phonenumber'], birthday = participantizer.data['birthday'], middlename = participantizer.data['middlename'], firstname = participantizer.data['firstname'], lastname = participantizer.data['lastname'], email = participantizer.data['email'], sex = participantizer.data['sex'], last_login = datetime.datetime.now())
            participant.set_password(participantizer.data['password'])
            participant.save()
            token = Token.objects.get(user=participant).key
            # resp = {}
            # resp['id'] = participant.id
            # resp['token'] = token
            confirmation_token = default_token_generator.make_token(participant)
            actiavation_link = f'83.221.202.194:2500/oborona/activate-account/?user_id={participant.id}&confirmation_token={confirmation_token}'
            message = get_template("emails/email_activation.html").render({'act_mail': actiavation_link})
            send_mail(
                # title:
                "Активация аккаунта участника фестиваля \"Оборона Таганрога 1855 года\"",
                # message:
                "\n",
                # "http:\\\\{}\n\nДля подтверждения почты перейдите по указанной ссылке, далее вернитесь в приложение и авторизуйтесь по почте и паролю, указанными при регистрации.\nЕсли Вы изменили свою почту на новую в профиле, авторизуйтесь в приложении с новой почтой, после того как её подтвердите.".format(actiavation_link),
                # from:
                "daniil-kochubey@yandex.ru",
                # to:
                [participant.email],


                html_message=message
            )
            print("USER DATA",participant.id, participantizer.data)
            return Response(status.HTTP_200_OK)
        # response = exception_handler(exc, context)
        # return Response(status.HTTP_400_BAD_REQUEST, context)


class ParticipantList(APIView):
    # permission_classes = [IsAuthenticated]
    #API that allows to view all Participants
    def get(self, request):
        queryset = Participant.objects.all()
        serializer = ParticipantSerializer(queryset, many = True)
        return Response(serializer.data)


class ParticipantDetail(APIView):
    # permission_classes = [IsAuthenticated]
    #API that allows to view single participant by pk
    def get(felf, request):
        
        pk = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').lstrip('Token ')).user_id   
        queryset = Participant.objects.get(id=pk)
        serializer = ParticipantDetailedSerializer(queryset)
        print(serializer.data)
        return Response(serializer.data)


class MyObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(MyObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'id': token.user_id, 'token': token.key})


# class ParticipantUpdate(generics.RetrieveUpdateAPIView):
#     #API that allows to update participant record
#     queryset = Participant.objects.all()
#     serializer_class = ParticipantSerializer


# class ParticipantDelete(generics.RetrieveDestroyAPIView):
#     #API that allows to delete participant record
#     queryset = Participant.objects.all()
#     serializer_class = ParticipantSerializer

#------------------------------------------------------------------
class ListCasualEvents(APIView):
#   permission_classes = [IsAuthenticated]
  def get(sels, request):
      events = Event.objects.filter(is_epic=False)
      serializer = EventCasualListSerializer(events, many=True)
      return Response(serializer.data)


class ListEpicEvents(APIView):
#   permission_classes = [IsAuthenticated]
  def get(sels, request):
      events = Event.objects.filter(is_epic=True)
      serializer = EventEpicListSerializer(events, many=True)
      return Response(serializer.data)


class ListAllEvents(APIView):
#   permission_classes = [IsAuthenticated]
  def get(sels, request):
      events = Event.objects.all()
      serializer = EventShortSerializer(events, many=True)
      return Response(serializer.data)


class EventCreate(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        event = EventCreateSerializer(data=request.data)
        if event.is_valid():
            event.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class EventAdminCreate(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        event = EventAdminCreateSerializer(data=request.data)
        if event.is_valid():
            event.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            print(event.errors.values())
        return Response(status=status.HTTP_400_BAD_REQUEST)


class EventDetail(APIView):
    def get(self, request, pk):
        events = Event.objects.get(id=pk)
        serialized_event = EventSerializer(events)
        return Response(serialized_event.data)

 
#формирование списка ролей с айдишниками и названиями вместо просто айдишников
        # roles = serialized_event.data["roles"]
        # roles_with_names = '{'
        # new_roles = []
        # for i in roles: new_roles.append(Role.objects.get(id=i))
        # for j in new_roles:
        #     serialized_role = RoleSerializer(j)
        #     roles_with_names = roles_with_names + "\""+str(serialized_role.data['id'])+"\": \"" + str(serialized_role.data["role_name"]) + "\","
        # roles_with_names = roles_with_names.rstrip(",") + "}"
        # newdata = dict(serialized_event.data)#
        # newdata.update({"roles": roles_with_names})
        # print(newdata)
#------------------------------------------------------------------

class RoleDetail(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        roles = Role.objects.get(id=pk)
        serializer = RoleSerializer(roles)
        return Response(serializer.data)

#------------------------------------------------------------------

class AdditionalInfoCreate(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        pk = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').lstrip('Token ')).user_id
        entry_serialized = EntryCreateSerializer(data={'event': 2, 'user':pk, 'role':5})
        print("INIITAL DATA FOR COSTUME")
        print(request.data)
        if entry_serialized.is_valid():
            entry_serialized.save()
        else:
            print(entry_serialized.errors)
            return Response(status.HTTP_400_BAD_REQUEST)#, data=entry_serialized.errors)
        request.data.update({'user': pk, 'entry':entry_serialized.data['id']})
        
        info = AdditionalInfoCreateSerializer(data=request.data)    
        if info.is_valid():
            info.save()
            return Response(status.HTTP_200_OK)
        print(info.errors)
        return Response(status.HTTP_400_BAD_REQUEST, data=info.errors)



#-----------------------------------------------------------------

class EntryCreate(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        serialized_entry = EntryCreateSerializer(data=request.data)
        if serialized_entry.is_valid():
            serialized_entry.save()
            return Response(status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)


class EntryList(APIView):
    # permission_classes = [IsAuthenticated]


    def get(self, request):
        pk = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').lstrip('Token ')).user_id
        entrys = Entry.objects.filter(user = pk)
        # print(entrys)
        serialized_entrys = EntryListSerializer(entrys, many=True)
        # print(serialized_entrys.data)
        # if serialized_entrys.is_valid(raise_exception=True):
        return Response(serialized_entrys.data)


#-----------------------------------------------------------------

class PromoCodeCreate(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, count):
        
        while count !=0:
            newCode = PromoCodes.create_code(number=count)
            data_for_serializer = {'code': newCode}
            serialized_code = PromoCodeSerializer(data=data_for_serializer)
            if serialized_code.is_valid():
                print("Noice")
                new_promo_code = PromoCodes.objects.create(code=serialized_code.data['code'])
                new_promo_code.save()
                count -= 1
            
        return Response(newCode)


class PromoCodeVerify(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        codes = PromoCodes.objects.filter(code=request.data['code'])
        pk = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').lstrip('Token ')).user_id
        user = Participant.objects.get(id=pk)
        user_with_code = PromoCodes.objects.filter(user=pk)
        
        if not codes:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="No such promocode")
        codes = codes[0]
        if user_with_code:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="You already activated promocode")
        elif codes.user != None:#update the object
            return Response(status=status.HTTP_400_BAD_REQUEST, data="No such promocode")        
        else:
            codes.user = user
            codes.save()
            user.is_sponsor = True
            user.save()
            return Response(status=200, data="Ok")


class MapPinsList(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        horecas = HoReCa.objects.all()
        events = Event.objects.all()
        
        serialized_horecas = HoReCaDetailSerializer(horecas, many=True)
        serialized_events = EventMapSerializer(events, many=True)
        return Response({
            "HoReCas":serialized_horecas.data,
            "Events":serialized_events.data
        })


class InfoWindowsList(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        info_windows_que = InfoWindow.objects.all()
        s_info_windows = InfoWindowListSerializer(info_windows_que, many=True)
        return Response(s_info_windows.data)


class InfoWindowsSingle(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        info_window = InfoWindow.objects.get(id=pk)
        s_info_window = InfoWindowSingleSerializer(info_window)
        return Response(s_info_window.data)


class TechInfoWindowImport(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        info_window = TechInfoWindowImportSerializer(data=request.data)
        if info_window.is_valid():
            info_window.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UnsubscribeFromEvent(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        
        pk = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').lstrip('Token ')).user_id
        req_data = request.data
        event_to_delete = Entry.objects.filter(event_id=req_data['event_id']).filter(user_id=pk)
        if event_to_delete:
            event_to_delete.delete()
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)

class ListRoles(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        all_roles = Role.objects.all()
        serialized_roles = RoleSerializer(all_roles, many=True)
        return Response(serialized_roles.data)


class CountSexes(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        ladys_count = 0
        gentleman_count = 0
        all_entrys = Entry.objects.all().filter(event=3)
        
        serialized_entrys = EntrysWithParticipantSerializer(all_entrys, many=True)
        print(serialized_entrys.data)
        for part in serialized_entrys.data:
            if part['user']['sex'] == 'f' and part['role'] == 7:
                ladys_count+=1
            if part['user']['sex'] == 'm' and part['role'] == 7:
                gentleman_count+=1
        resp={'woman': ladys_count, 'man': gentleman_count}
        return Response(resp, status=status.HTTP_200_OK)

class ParticipantUpdate(APIView, UpdateModelMixin):
    # permission_classes = [IsAuthenticated]
    queryset = Participant.objects.all()
    serializer_class = ParticipantCreateSerializer

    # def patch(self, request, *args, **kwargs):
    #     pk = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').lstrip('Token ')).user_id
    #     user_instance = Participant.objects.get(id=pk)
    #     user_instance.partial_update(request, *args, **kwargs)
    #     return Response(200)
    #     return self.partial_update(request, *args, **kwargs)
    
    # # def get_object(self, *args, **kwargs):
        
    def patch(self, request):
        pk = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').lstrip('Token ')).user_id
        user_instance = Participant.objects.get(id=pk)
        # user_instance['name'].update("Вася")
        serialized_participant= ParticipantUpdateSerializer(user_instance, data=request.data, partial=True)
        
        print(user_instance)
        if serialized_participant.is_valid(raise_exception=True):
            
            serialized_participant.save()
            pass
        serialized_participant.save()
        # part_serialized = ParticipantDetailedSerializer(user_instance)
        print(serialized_participant.data)
        # user_instance.perform_update(serialized_participant)
        return Response(status=status.HTTP_200_OK)

class ParticipantUpdateEmail(APIView):
    def post(self, request):
        pk = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').lstrip('Token ')).user_id
        user_instance = Participant.objects.get(id=pk)
        newEmail = request.data['email']
        
        user_instance.email = newEmail
        user_instance.is_active = False
        user_instance.save()
        confirmation_token = default_token_generator.make_token(user_instance)
        actiavation_link = f'83.221.202.194:2500/oborona/activate-account/?user_id={user_instance.id}&confirmation_token={confirmation_token}'
        message = message = get_template("emails/email_activation.html").render({'act_mail': actiavation_link})
        send_mail(
                # title:
                "Активация аккаунта участника фестиваля \"Оборона Таганрога 1855 года\"",
                # message:
                "{}\nЕсли Вы изменили свою почту на новую в профиле, авторизуйтесь в приложении с новой почтой, после того как её подтвердите.".format(actiavation_link),
                # from:
                "daniil-kochubey@yandex.ru",
                # to:
                [newEmail],

                html_message=message
            )
        return Response(status.HTTP_200_OK)


class ParticipantCangePassword(APIView):
    def post(self, request):
        pk = Token.objects.get(key = request.META.get('HTTP_AUTHORIZATION').lstrip('Token ')).user_id
        request.data.update({"pk": pk})

        ser_pass = ChangePasswordSerializer(data = request.data)
        if ser_pass.is_valid(raise_exception=True):
            ser_pass.save(validated_data=ser_pass.validated_data)
        return Response(status.HTTP_200_OK)


class ActivateParticipantByLink(APIView):
    # permission_classes = [AllowAny]
    def get(self, request):
        participant_id = request.query_params.get('user_id', '')
        # participant = Participant.objects.get(id = participant_id)
        confirmation_token = request.query_params.get('confirmation_token', '')
        participant = Participant.objects.get(id=participant_id)
        if participant == None:
            return Response(status.HTTP_400_BAD_REQUEST)
        if not default_token_generator.check_token(participant, confirmation_token):
            return Response(status.HTTP_400_BAD_REQUEST)
        participant.is_active = True
        participant.save()
        return Response(status.HTTP_200_OK)

# Site
#----------------------------------------------------------------------------------------------------------------------------------------#
def horeca(request):
    queryset = HoReCa.objects.all()

    context = {
        "welcome": "Партнёры HoReCa", 
        "queryset": queryset
    }
    return render(request, 'oborona_taganroga/horeca.html', context=context)


def people(request):
    queryset = Participant.objects.all()

    # Не выводим
    # birthday, password, entrys, is_admin, is_active, last_login

    context = {
        "welcome": "Участники фестиваля",
        "queryset": queryset
    }
    return render(request, 'oborona_taganroga/people.html', context=context)

def events(request):
    queryset = Event.objects.all()

    # Не выводим
    # is_epic

    context = {
        "welcome": "События фестиваля",
        "queryset": queryset
    }
    return render(request, 'oborona_taganroga/events.html', context=context)

def how_to_use(request):
    context = {
        "welcome": "Как пользоваться сайтом",
    }
    return render(request, 'oborona_taganroga/how_to_use.html', context=context)

def download_people(request):
    queryset = Participant.objects.all()
    serializer = ParticipantSerializerSite(queryset, many = True)

    # Создание excel файла
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'people.xlsx'
    filepath = BASE_DIR + '/oborona_taganroga/files/' + filename
    
    size = 'A1:G'+str(len(serializer.data) + 1)
    workbook = xlsxwriter.Workbook(filepath)
    worksheet = workbook.add_worksheet()
    worksheet.add_table(size, {'autofilter': False, 'columns': 
                                         [{'header': 'Имя'},
                                          {'header': 'Фамилия'},
                                          {'header': 'Отчество'},
                                          {'header': 'Телефон'},
                                          {'header': 'Пол'},
                                          {'header': 'Электронная почта'},
                                          {'header': 'Спонсор'},
                                          ]})

    # Настройка размеров отображения таблицы
    cell_format = workbook.add_format()
    cell_format.set_text_wrap()
    worksheet.set_column('A:G', 30)

    # Запись в Excel файл
    row,col = 1,0

    # Добавить сюда код чтобы всё было норм
    for item in serializer.data:
        worksheet.write(row, col, item['firstname'],cell_format)
        worksheet.write(row, col + 1, item['lastname'],cell_format)
        worksheet.write(row, col + 2, item['middlename'],cell_format)
        worksheet.write(row, col + 3, item['phonenumber'],cell_format)
        worksheet.write(row, col + 4, item['sex'],cell_format)
        worksheet.write(row, col + 5, item['email'],cell_format)
        worksheet.write(row, col + 6, item['is_sponsor'],cell_format)
        row += 1
    workbook.close()

    # Отправляем сформированный документ
    if os.path.exists(filepath):
        with open(filepath, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = 'attachment; filename=people.xlsx'
            return response

def download_events(request):
    queryset = Event.objects.all()
    serializer = EventSerializerSite(queryset, many = True)

    # Создание excel файла
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'events.xlsx'
    filepath = BASE_DIR + '/oborona_taganroga/files/' + filename
   
    size = 'A1:K'+str(len(serializer.data) + 1)
    workbook = xlsxwriter.Workbook(filepath)
    worksheet = workbook.add_worksheet()
    worksheet.add_table(size, {'autofilter': False, 'columns': 
                                         [{'header': 'Название'},
                                          {'header': 'Иллюстрация'},
                                          {'header': 'Краткое описание'},
                                          {'header': 'Полное описание'},
                                          {'header': 'Адрес'},
                                          {'header': 'Старт'},
                                          {'header': 'Финиш'},
                                          {'header': 'Роли'},
                                          {'header': 'Широта'},
                                          {'header': 'Долгота'},
                                          {'header': 'Телефонный номер'},
                                          ]})

    # Настройка размеров отображения таблицы
    cell_format = workbook.add_format()
    cell_format.set_text_wrap()
    worksheet.set_column('A:K', 30)

    # Запись в Excel файл
    row,col = 1,0

    # Добавить сюда код чтобы всё было норм
    for item in serializer.data:
        worksheet.write(row, col, item['name'],cell_format)
        worksheet.write(row, col + 1, item['pic_url'],cell_format)
        worksheet.write(row, col + 2, item['brief_disc'],cell_format)
        worksheet.write(row, col + 3, item['full_disc'],cell_format)
        worksheet.write(row, col + 4, item['adress'],cell_format)
        worksheet.write(row, col + 5, item['time_start'],cell_format)
        worksheet.write(row, col + 6, item['time_end'],cell_format)

        # Тут надо отедльную обработку для ролей придумать
        print(item['roles'])
        
        worksheet.write(row, col + 8, item['coord_long'],cell_format)
        worksheet.write(row, col + 9, item['coord_lat'],cell_format)
        worksheet.write(row, col + 10, item['phonenumber'],cell_format)
        row += 1
    workbook.close()

    # Отправляем сформированный документ
    if os.path.exists(filepath):
        with open(filepath, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = 'attachment; filename=events.xlsx'
            return response

def download_horeca(request):

    # Формируем excel
    queryset = HoReCa.objects.all()
    serializer = HoReCaDetailSerializer(queryset, many = True)

    # Создание excel файла
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'horeca.xlsx'
    filepath = BASE_DIR + '/oborona_taganroga/files/' + filename

    # size = 'A1:Е'+str(len(serializer.data) + 1)
    size = 'A1:E'+str(len(serializer.data) + 1)
    workbook = xlsxwriter.Workbook(filepath)
    worksheet = workbook.add_worksheet()
    worksheet.add_table(size, {'autofilter': False, 'columns': 
                                         [{'header': 'Название'},
                                          {'header': 'Описание'},
                                          {'header': 'Широта'},
                                          {'header': 'Долгота'},
                                          {'header': 'Мобильный'},
                                          ]})


    # Настройка размеров отображения таблицы
    cell_format = workbook.add_format()
    cell_format.set_text_wrap()
    worksheet.set_column('A:E', 30)

    # Запись в Excel файл
    row,col = 1,0

    # Добавить сюда код чтобы всё было норм
    for item in serializer.data:
        worksheet.write(row, col, item['name'],cell_format)
        worksheet.write(row, col + 1, item['discription'],cell_format)
        worksheet.write(row, col + 2, item['coord_long'],cell_format)
        worksheet.write(row, col + 3, item['coord_lat'],cell_format)
        worksheet.write(row, col + 4, item['phonenumber'],cell_format)
        row += 1
    workbook.close()

    # Отправляем сформированный документ
    if os.path.exists(filepath):
        with open(filepath, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = 'attachment; filename=horeca.xlsx'
            return response

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'oborona_taganroga/name.html', {'form': form})