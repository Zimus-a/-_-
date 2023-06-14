from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token    
from .views import *

# Site
from .views import horeca, people, events

app_name = 'oborona'

urlpatterns = [
    path('participantcreate/', ParticipantCreate.as_view(), name='create-participant'),
    path('participants/', ParticipantList.as_view()),
    path('participant/', ParticipantDetail.as_view(), name='retrieve-participant'),
    # path('participantupdate/<int:pk>/', ParticipantUpdate.as_view(), name='update-participant'),
    
    path('eventcreate/', EventCreate.as_view(), name='create-event'),
    path('eventadmincreate/', EventAdminCreate.as_view(), name='create-admin-event'),
    path('casualevents/', ListCasualEvents.as_view(), name='casual-event'),
    path('epicevents/', ListEpicEvents.as_view(), name='epic-event'),
    path('event/<int:pk>/', EventDetail.as_view(), name='retrieve-event'),
    path('eventsall/', ListAllEvents.as_view(), name='all-events'),

    # path('delete/<int:pk>/', ParticipantDelete.as_view(), name='delete-participant')

    path('role/<int:pk>', RoleDetail.as_view(), name='retrieve-role'),

    path('info/', AdditionalInfoCreate.as_view(), name='create-info'),

    path('entrycreate/', EntryCreate.as_view(), name='create-entry'),

    path('promocodecreate/<int:count>', PromoCodeCreate.as_view(), name='create-promocode'),
    path('promocodeverify/', PromoCodeVerify.as_view(), name='verify-promocode'),

    path('entrys/', EntryList.as_view(), name='list-entrys'),
    path('map/', MapPinsList.as_view(), name='mappin-list'),

    
    path('importinfowindow/', TechInfoWindowImport.as_view(), name='import-infowindows'),
    path('infowindowlist/', InfoWindowsList.as_view()),
    path('infowindow/<int:pk>', InfoWindowsSingle.as_view()),

    path('unsubscribe/', UnsubscribeFromEvent.as_view()),


    path('listroles/', ListRoles.as_view()),
    path('costume/', AdditionalInfoCreate.as_view()),

    path('sexcount/', CountSexes.as_view()),

    path('participantupdate/', ParticipantUpdate.as_view()),
    path('participantupdateemail/', ParticipantUpdateEmail.as_view()),
    path('participantchangepassword/', ParticipantCangePassword.as_view()),

    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('api-token-auth/', MyObtainAuthToken.as_view(), name='login'),

    path('activate-account/', ActivateParticipantByLink.as_view()),


    # Site
    path('people/', people, name='people'),
    path('events/', events, name='events'),
    path('horeca/', horeca, name='horeca'),
    path('how_to_use/', how_to_use, name='how_to_use'),
    path('download_people/', download_people, name='download_people'),
    path('download_events/', download_events, name='download_events'),
    path('download_horeca/', download_horeca, name='download_horeca'),
    path('get_name/', get_name, name='get_name'),
]

