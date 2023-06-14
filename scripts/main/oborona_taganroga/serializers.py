from pyexpat import model
from rest_framework import serializers
from .models import *


class ParticipantCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant
        fields = ['firstname', 'lastname', 'middlename', 'email', 'password', 'sex', 'phonenumber', 'birthday']


class ParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant
        fields = ['pk', 'firstname', 'middlename', 'birthday']


class ParticipantDetailedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant
        exclude = ['password']

class ParticipantSerializerSite(serializers.ModelSerializer):

    class Meta:
        model = Participant
        fields = ['firstname', 'lastname', 'middlename', 'phonenumber', 'sex', 'email', 'is_sponsor']



# --------------------------------------------------------------------------------ы

class EventCasualListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['pk', 'name', 'brief_disc', 'pic_url']


class EventEpicListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['pk', 'name', 'pic_url']


class EventShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['id', 'name', 'brief_disc', 'time_start', 'time_end', 'coord_lat', 'coord_long', 'phonenumber']


class EventCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['name', 'brief_disc', 'adress']

class EventAdminCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['name', 'pic_url', 'brief_disc', 'full_disc', 'adress', 'time_start', 'coord_long', 'coord_lat', 'roles']

class EventMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['id', 'name','adress', 'time_start', 'time_end', 'coord_lat', 'coord_long']
# --------------------------------------------------------------------------------

class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'#['role_name', 'info']

class RoleShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['role_name']


class RoleInEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['id', 'role_name']

# --------------------------------------------------------------------------------
    
class AdditionalInfoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdditionalInfo
        exclude = ['id']
    
    # def validate(self, data):
    #     if (data['chest'] < 0 or data['chest'] > 200) and data['chest'] != None:
    #         raise serializers.ValidationError("chest must be value non less than 0 and not bigger than 200")
    #     if (data['waist'] < 0 or data['waist'] > 200) and data['waist'] != None:
    #         raise serializers.ValidationError("waist must be value non less than 0 and not bigger than 200")
    #     if (data['hips'] < 0 or data['hips'] > 200) and data['hips'] != None:
    #         raise serializers.ValidationError("hips must be value non less than 0 and not bigger than 200")
    #     if (data['height'] < 55 or data['height'] > 251) and data['height'] != None:
    #         raise serializers.ValidationError("height must be value non less than 55 and not bigger than 251")
    #     if (data['shoe_size'] < 20 or data['shoe_size'] > 60) and data['shoe_size'] != None:
    #         raise serializers.ValidationError("shoe_size must be value non less than 20 and not bigger than 60")
        
    #     return data

#----------------------------------------------------------------------------------

class HoReCaSerializer(serializers.ModelSerializer):

    class Meta:
        model = HoReCa
        fields = {'id', 'coord_long', 'coord_lat'}

class HoReCaDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = HoReCa
        fields = '__all__'
#----------------------------------------------------------------------------------

class EventSerializer(serializers.ModelSerializer):
    roles = RoleInEventSerializer(many=True)
    class Meta:
        model = Event
        fields = ['id', 'name', 'pic_url', 'brief_disc', 'full_disc', 'adress',
         'time_start', 'time_end', 'roles', 'coord_long', 'coord_lat', 'is_epic', 'phonenumber']

class EventSerializerSite(serializers.ModelSerializer):
    # roles = RoleInEventSerializer(many=True)
    class Meta:
        model = Event
        fields = ['name', 'pic_url', 'brief_disc', 'full_disc', 'adress', 'time_start', 'time_end', 'roles', 'coord_long', 'coord_lat', 'phonenumber']


class EntryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = '__all__'


class PromoCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PromoCodes
        fields = '__all__'


class EntryListSerializer(serializers.ModelSerializer):
    role = RoleShortSerializer()
    event = EventShortSerializer()
    class Meta:
        model = Entry
        fields = ['event','role']

#----------------------------------------------------------------------------------

class InfoWindowListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoWindow
        fields = ['id', 'name']

class InfoWindowSingleSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoWindow
        fields = '__all__'

class TechInfoWindowImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoWindow
        fields = '__all__'


    
class FilterLadySerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(sex='f')
        return super(FilterLadySerializer, self).to_representation(data)


class ParticipantEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant
        fields = ['pk', 'sex']


class EntrysWithParticipantSerializer(serializers.ModelSerializer):
    # womans = 
    user = ParticipantEntrySerializer()
    class Meta:
        model = Entry
        fields = '__all__'


class ParticipantUpdateSerializer(serializers.ModelSerializer):
    # womans = 
    
    class Meta:
        model = Participant
        exclude = ['password']# , 'email'


class ParticipantUpdateEmailSerializer(serializers.ModelSerializer):
    # womans = 
    
    class Meta:
        model = Participant
        exclude = ['password']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=120, write_only=True, required=True)
    new_password = serializers.CharField(max_length=120, write_only=True, required=True)
    
    pk = serializers.DecimalField(max_digits=10, decimal_places=0)
    # def validate_old_password(self, data):
    #     print(data)
    #     user = Participant.objects.get(id=data['pk'])
    #     # user = self.context['request'].user
    #     if not user.check_password(data['old_password']):
    #         raise serializers.ValidationError(
    #             _('Your old password was entered incorrectly. Please enter it again.')
    #         )
    #     return value

    def validate(self, data):
        user = Participant.objects.get(id=data['pk'])
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({'password': 'Your old password was entered incorrectly. Please enter it again.'}            )
        
        return data

    def save(self, validated_data):

        password = self.validated_data['new_password']
        user = Participant.objects.get(id=validated_data['pk'])
        
        user.set_password(password)
        user.save() 
        return user