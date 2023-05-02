from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from vtx.models import Gateway  # pega as caracteristicas fisicas do dxm
from .protocolo import Protocolo 

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getRelogio(request):
    try:        
        endereco = Gateway.objects.all().first()
        dxm = Protocolo(endereco.port)
        data = {
            'valor':str(dxm.getRelogio()),
            'erro': False
        }
        endereco.online = True
        endereco.save()
    except Exception as EX:
        data = {
            'valor': '',
            'erro': str(EX)
        }
        endereco.online = False
        endereco.save()
    return Response(data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def setRelogio(request):
    try:        
        endereco = Gateway.objects.all().first()
        dxm = Protocolo(endereco.port)
        data = {
            'valor':str(dxm.setRelogio()),
            'erro': False
        }
        endereco.online = True
        endereco.save()
    except Exception as EX:
        data = {
            'valor': False,
            'erro': str(EX)
        }        
        endereco.online = False
        endereco.save()
    return Response(data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Reboot(request):
    try:        
        endereco = Gateway.objects.all().first()
        dxm = Protocolo(endereco.port)
        data = {
            'valor':str(dxm.reboot()),
            'erro': False
        }
        endereco.online = True
        endereco.save()
    except Exception as EX:
        data = {
            'valor': False,
            'erro': str(EX)
        }        
        endereco.online = False
        endereco.save()        
    return Response(data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Travar(request):
    try:        
        endereco = Gateway.objects.all().first()
        dxm = Protocolo(endereco.port)
        data = {
            'valor':str(dxm.travar()),
            'erro': False
        }
        endereco.online = True
        endereco.save()
    except Exception as EX:
        data = {
            'valor': False,
            'erro': str(EX)
        }        
        endereco.online = False
        endereco.save()        
    return Response(data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Destravar(request):
    try:        
        endereco = Gateway.objects.all().first()
        dxm = Protocolo(endereco.port)
        data = {
            'valor':str(dxm.destravar),
            'erro': False
        }
        endereco.online = True
        endereco.save()
    except Exception as EX:
        data = {
            'valor': False,
            'erro': str(EX)
        }        
        endereco.online = False
        endereco.save()        
    return Response(data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getRegs(request):
    try:
        reg = int(request.POST['registro'])  
        qtd = int(request.POST['quantidade']) 
        id = int(request.POST['modbusid'])         
        endereco = Gateway.objects.all().first()
        dxm = Protocolo(endereco.port)
        data = {
            'valor': str(dxm.readReg(reg,qtd,slaveID=id)),
            'erro': False
        }
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
def setRegs(request):
    try:
        reg = int(request.POST['registro'])  
        id = int(request.POST['modbusid']) 
        arrey_str = str(request.POST['ar'])   
        arrey = arrey_str.split(',')   
        print(arrey)   
        endereco = Gateway.objects.all().first()
        dxm = Protocolo(endereco.port)
        data = {
            'valor': str(dxm.writeReg(reg,arrey,slaveID=id)),
            'erro': False
        }
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

