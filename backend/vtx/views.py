from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import OsSerializer
from .serializer import GatewaySerializer, NodeSerializer, NodeSetupSerializer, HistSerializer, EventoSerializer
from django.shortcuts import HttpResponse
from django.views.generic import View
from django.db.models import Q
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import OS
from .models import Gateway, Node, NodeSetup, Hist, Evento

from .cicloLeitura import *

class OsList(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset = OS.objects.all()
    serializer_class = OsSerializer

class OsDetail(generics.RetrieveUpdateDestroyAPIView):    
    permission_classes=[IsAuthenticated]
    queryset = OS.objects.all()
    serializer_class = OsSerializer

class GatewayList(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Gateway.objects.all()
    serializer_class = GatewaySerializer

class GatewayDetail(generics.RetrieveUpdateDestroyAPIView):    
    permission_classes=[IsAuthenticated]
    queryset = Gateway.objects.all()
    serializer_class = GatewaySerializer

class NodeList(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

class NodeDetail(generics.RetrieveUpdateDestroyAPIView):    
    permission_classes=[IsAuthenticated]
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

class NodeSetupList(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset = NodeSetup.objects.all()
    serializer_class = NodeSetupSerializer

class NodeSetupDetail(generics.RetrieveUpdateDestroyAPIView):    
    permission_classes=[IsAuthenticated]
    queryset = NodeSetup.objects.all()
    serializer_class = NodeSetupSerializer

class HistList(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Hist.objects.all()
    serializer_class = HistSerializer

class HistDetail(generics.RetrieveUpdateDestroyAPIView):    
    permission_classes=[IsAuthenticated]
    queryset = Hist.objects.all()
    serializer_class = HistSerializer

class EventoList(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

class EventoDetail(generics.RetrieveUpdateDestroyAPIView):    
    permission_classes=[IsAuthenticated]
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def DxmStatus(request):
    modelo = Gateway.objects.all()[0]
    data = {
        'online':modelo.online,
        'nome': modelo.name,
        'configurar': modelo.configurar,
        'percent': modelo.configurarStatus,
        'msg': modelo.configurarMsg,
    }
    return Response(data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Aprende(request):
    endereco =Gateway.objects.all()[0]
    try:
        reg = int(request.POST['alvo'])  
        data = {
            'valor': "ok",
            'erro': False
        }
        endereco.aprender = True
        endereco.motorIndex = reg
        endereco.online = True
        endereco.save()
    except Exception as EX:
        data = {
            'valor': 'erro',
            'erro': str(EX)
        }        
        endereco.online = False
        endereco.save()        
    return Response(data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ConfigDXM(request):
    endereco =Gateway.objects.all()[0]
    try:
        data = {
            'valor': "ok",
            'erro': False
        }
        endereco.configurar = True
        endereco.online = True
        endereco.save()
    except Exception as EX:
        data = {
            'valor': 'erro',
            'erro': str(EX)
        }        
        endereco.online = False
        endereco.save()        
    return Response(data)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Filtra(request):
    try:
        inis = str(request.POST['ini'])
        fims = str(request.POST['fim'])
        node = int(request.POST['node'])
        print(f'{inis}')
        print(f'{fims}')
        if inis == '':
            agora = datetime.now()
            inis = f'{agora.year}-{agora.month}-{agora.day}T0:0:0'
            fims = f'{agora.year}-{agora.month}-{agora.day}T23:59:0'
        iniDA=inis.split('T')[0].split('-')
        iniTA=inis.split('T')[1].split(':')
        fimDA=fims.split('T')[0].split('-')
        fimTA=fims.split('T')[1].split(':')
        ini = datetime(int(iniDA[0]),int(iniDA[1]),int(iniDA[2]),int(iniTA[0]),int(iniTA[1]),0)
        fim = datetime(int(fimDA[0]),int(fimDA[1]),int(fimDA[2]),int(fimTA[0]),int(fimTA[1]),0)
        ini += timedelta(hours=3)
        fim += timedelta(hours=3)
        hist = Hist.objects.filter(Q(time__gt=ini) & Q(time__lt=fim) & Q(node=node)).order_by('time')
        histSerial = HistSerializer(hist, many=True)
        obj = histSerial.data
        return Response(obj)
    except Exception as EX:
        return Response(data = {'erro':str(EX)})

@method_decorator(csrf_exempt, name='dispatch')
class Eventos(View):
    def post(self,request):
        inis = str(request.POST['ini'])
        fims = str(request.POST['fim'])
        print(f'{inis}')
        print(f'{fims}')
        if inis == '':
            agora = datetime.now()
            inis = f'{agora.year}-{agora.month}-{agora.day}T0:0:0'
            fims = f'{agora.year}-{agora.month}-{agora.day}T23:59:0'
        iniDA=inis.split('T')[0].split('-')
        iniTA=inis.split('T')[1].split(':')
        fimDA=fims.split('T')[0].split('-')
        fimTA=fims.split('T')[1].split(':')
        ini = datetime(int(iniDA[0]),int(iniDA[1]),int(iniDA[2]),int(iniTA[0]),int(iniTA[1]),0)
        fim = datetime(int(fimDA[0]),int(fimDA[1]),int(fimDA[2]),int(fimTA[0]),int(fimTA[1]),0)
        ini += timedelta(hours=3)
        fim += timedelta(hours=3)
        print(f'{ini}')
        print(f'{fim}')
        dadof = Evento.objects.filter(Q(date__gt=ini) & Q(date__lt=fim)).order_by('date')
        strinfy = ""
        
        for hf in dadof:
            hora = int(hf.date.hour)-3
            if hora<0:
                hora+=23  
            hf.date = f'{hora}:{hf.date.minute} {hf.date.day}/{hf.date.month}/{hf.date.year}'
            strinfy = f'{strinfy}{{"hora":"{hf.date}","Node":"{hf.node}","Tipo":"{hf.tipo}","Evento":"{hf.descricao}"}},'
        strinfy = "[" + strinfy[:len(strinfy)-1] + "]"
        return HttpResponse(strinfy)

