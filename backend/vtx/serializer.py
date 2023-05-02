from rest_framework import serializers
from .models import OS
from .models import Gateway, Node, NodeSetup, Evento, Hist
from datetime import datetime, timedelta

class OsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OS
        fields = '__all__'

class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateway
        fields = '__all__'

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'

class NodeSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeSetup
        fields = '__all__'

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

class HistSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()

    class Meta:
        model = Hist
        fields = ('node','time','vibraX','vibraZ','temp','vibraZ2','vibraX2','corrente','alertVibraX','alertVibraZ','alertTemp','alertVibraZ2','alertVibraX2','alertCorrente')
    def get_time(self,obj):
        valor = obj.time
        return f'{valor.hour}:{valor.minute}  {valor.day}/{valor.month}/{valor.year}'
    def to_representation(self, instance):
        valor = instance.time - timedelta(hours=3)
        info = NodeSetup.objects.get(node=Node.objects.get(id=int(instance.node.id)))
        return {
            'Hora': f'{valor.hour}:{valor.minute}  {valor.day}/{valor.month}/{valor.year}',
            'X RMS': instance.vibraX/info.fatorVibraX,
            'Z RMS': instance.vibraZ/info.fatorVibraZ,
            'X Pico': instance.vibraX2/info.fatorVibraX2,
            'Z Pico': instance.vibraZ2/info.fatorVibraZ2,
            'T': instance.temp/info.fatorTemp,
            'A': instance.corrente/info.fatorCorrente,
            'X RMS alm': instance.alertVibraX/info.fatorVibraX,
            'Z RMS alm': instance.alertVibraZ/info.fatorVibraZ,
            'X Pico alm': instance.alertVibraX2/info.fatorVibraX2,
            'Z Pico alm': instance.alertVibraZ2/info.fatorVibraZ2,
            'T alm': instance.alertTemp/info.fatorTemp,
            'A alm': instance.alertCorrente/info.fatorCorrente,
        }