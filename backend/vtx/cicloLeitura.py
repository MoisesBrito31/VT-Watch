from .models import Gateway, Hist, Node, NodeSetup, Aprendizado,AprendizadoLog
from time import sleep
from threading import Thread
from datetime import datetime
from dxm.protocolo import Protocolo
import json


def criarScript():
    dispo = Node.objects.all()
    dispoConfig = NodeSetup.objects.all()
    dados = f'quantidade={len(dispo)}\r'
    index = 0
    for x in dispo:
        info = dispoConfig.get(node=x)
        dados = f'{dados}vibraX[{index}]=0\r'
        dados = f'{dados}vibraZ[{index}]=0\r'
        dados = f'{dados}vibraX2[{index}]=0\r'
        dados = f'{dados}vibraZ2[{index}]=0\r'
        dados = f'{dados}temp[{index}]=0\r'
        dados = f'{dados}corrente[{index}]=0\r'
        dados = f'{dados}estado[{index}]=0\r'
        dados = f'{dados}alerta[{index}]=0\r'
        dados = f'{dados}online[{index}]=0\r'
        dados = f'{dados}nodeId[{index}]={x.id}\r'
        dados = f'{dados}endereco[{index}]={info.address}\r'
        dados = f'{dados}ciclo[{index}]={info.ciclo}\r'
        dados = f'{dados}cicloConter[{index}]=0\r'
        dados = f'{dados}addrVibraX[{index}]={info.addrVibraX}\r'
        dados = f'{dados}addrVibraX2[{index}]={info.addrVibraX2}\r'
        dados = f'{dados}addrVibraZ[{index}]={info.addrVibraZ}\r'
        dados = f'{dados}addrVibraZ2[{index}]={info.addrVibraZ2}\r'
        dados = f'{dados}addrTemp[{index}]={info.addrTemp}\r'
        dados = f'{dados}addrCorrente[{index}]={info.addrCorrente}\r'
        dados = f'{dados}alertVibraX[{index}]={int(info.alertVibraX)}\r'
        dados = f'{dados}alertVibraX2[{index}]={int(info.alertVibraX2)}\r'
        dados = f'{dados}alertVibraZ[{index}]={int(info.alertVibraZ)}\r'
        dados = f'{dados}alertVibraZ2[{index}]={int(info.alertVibraZ2)}\r'
        dados = f'{dados}alertTemp[{index}]={int(info.alertTemp)}\r'
        dados = f'{dados}alertCorrente[{index}]={int(info.alertCorrente)}\r'
        dados = f'{dados}alertVibraXNv2[{index}]={int(info.alertVibraXNv2)}\r'
        dados = f'{dados}alertVibraX2Nv2[{index}]={int(info.alertVibraX2Nv2)}\r'
        dados = f'{dados}alertVibraZNv2[{index}]={int(info.alertVibraZNv2)}\r'
        dados = f'{dados}alertVibraZ2Nv2[{index}]={int(info.alertVibraZ2Nv2)}\r'
        dados = f'{dados}alertTempNv2[{index}]={int(info.alertTempNv2)}\r'
        dados = f'{dados}alertCorrenteNv2[{index}]={int(info.alertCorrenteNv2)}\r'
        dados = f'{dados}aprender[{index}]=0\r'
        dados = f'{dados}aprenderTime[{index}]={int(info.aprenderTime)}\r'
        dados = f'{dados}aprenderTimeConter[{index}]=0\r'
        dados = f'{dados}aprenderCiclo[{index}]={int(info.aprenderCiclo)}\r'
        dados = f'{dados}aprenderConter[{index}]=0\r'
        index = index+1
    VTFile = open("VT.sb",'r')
    dados = f'{dados}\r{VTFile.read()}'
    VTFile.close()
    arquivo = open("scriptVT.sb",'w')
    arquivo.write(dados)
    arquivo.close()


def leitura():
    controle = True
    while controle:
        try:
            sleep(2)
            ip = Gateway.objects.all()[0]
            nodes = Node.objects.all()
            index = 0
            for n in nodes:
                dxm = Protocolo(ip.port)
                info = NodeSetup.objects.get(node=n.id)
                # aqui verifica se o usuario quer iniciar aprendizado de um motor
                if ip.aprender:
                    if ip.motorIndex == n.id:
                        sleep(1)
                        dxm.writeReg(index*50+10,[1],slaveID=199)
                        sleep(1)
                        ip.aprender = 0
                        ip.motorIndex = 0
                        ip.save()
                n.vibraX = int(dxm.readReg(index*50+1,1,slaveID=199)[0])/info.fatorVibraX
                n.vibraZ = int(dxm.readReg(index*50+2,1,slaveID=199)[0])/info.fatorVibraZ
                n.vibraX2 = int(dxm.readReg(index*50+3,1,slaveID=199)[0])/info.fatorVibraX2
                n.vibraZ2 = int(dxm.readReg(index*50+4,1,slaveID=199)[0])/info.fatorVibraZ2
                n.temp = int(dxm.readReg(index*50+5,1,slaveID=199)[0])/info.fatorTemp
                n.corrente = int(dxm.readReg(index*50+6,1,slaveID=199)[0])/info.fatorCorrente
                n.alerta = dxm.readReg(index*50+7,1,slaveID=199)[0]
                while len(n.alerta)<6:
                    n.alerta = f'0{n.alerta}'
                n.estado = str(dxm.readReg(index*50+8,1,slaveID=199)[0])
                if str(dxm.readReg(index*50+9,1,slaveID=199)[0]) == "1":
                    n.online = True
                else:
                    n.online = False
                n.save()
                index = index+1
            # realiza o log
            if dxm.fileExist("SbFile1.dat"):
                sleep(2)
                info = dxm.getFile("SbFile1.dat")
                linhas = 0
                data = ''
                corrompido = False
                for x in info:
                    linhas +=1
                    data = f'{data}{str(x)}'
                    #print(f'linhas recebidas{linhas}, tem falha: {x.count("falha crc")}\r\n')
                    if x.count("falha crc")>0:
                        corrompido = True
                if not corrompido:
                    data = f'[{data[:len(data)-1]}]'
                    obj = json.loads(data)
                    for x in obj:
                        h = Hist(
                            node=Node.objects.get(id=int(x['node'])), 
                            time=datetime.strptime(x['time'],'%Y-%m-%d %H:%M:%S'),
                            vibraX = int(x['vibraX']),
                            vibraX2 = int(x['vibraX']),
                            vibraZ = int(x['vibraZ']),
                            vibraZ2 = int(x['vibraZ2']),
                            temp = int(x['temp']),
                            corrente = int(x['corrente']),
                            alertVibraX = int(x['alertVibraX']),
                            alertVibraX2 = int(x['alertVibraX']),
                            alertVibraZ = int(x['alertVibraZ']),
                            alertVibraZ2 = int(x['alertVibraZ2']),
                            alertTemp = int(x['alertTemp']),
                            alertCorrente = int(x['alertCorrente']),
                        )
                        h.save()
                    print("apagando Arquivo")
                    dxm.deleteFile("SbFile1.dat")
                    sleep(1)
                    while dxm.fileExist("SbFile1.dat"):
                         dxm.deleteFile("SbFile1.dat")
                         print("tentando novamente apagar LOG...")
                         sleep(5)
                    print("executou log")
            
            # realiza o processo de programar o DXM:
            if ip.configurar:
                criarScript()
                ip.configurarStatus = 10
                ip.configurarMsg = "iniciando"
                ip.save()
                sleep(5)
                if dxm.enviaArquivo("scriptVT.sb",""):
                    ip.configurarStatus = 40
                    ip.configurarMsg = "Script Carregado"
                    ip.save()
                    sleep(5)
                    if dxm.enviaArquivo("DXMConfig.xml",""):
                        ip.configurarStatus = 60
                        ip.configurarMsg = "XML Carregado"
                        ip.save()
                        sleep(5)                        
                        ip.configurarStatus = 100
                        ip.configurarMsg = "Reboot DXM"
                        ip.save()
                        dxm.reboot()
                        sleep(10)
                        ip.configurarMsg = "ok"
                    else:
                        ip.configurarStatus = 0
                        ip.configurarMsg = "Falha ao enviar Script"
                        sleep(5)
                else:
                    ip.configurarStatus = 0
                    ip.configurarMsg = "Falha ao enviar XML"
                    sleep(5)

            # verifica se uma aprendizagem esta concluida:
            if dxm.fileExist("SbFile2.dat"):
                for n in range(len(nodes)):
                    if int(dxm.readReg(n*50+10,1,slaveID=199)[0]) == 0:
                        print("\r\r\r\rvou aprender AGORA\r\r\r\r")
                        info = dxm.getFile("SbFile2.dat")
                        linhas = 0
                        data = ''
                        corrompido = False
                        for x in info:
                            linhas +=1
                            data = f'{data}{str(x)}'
                            print(f'linhas recebidas{linhas}, tem falha: {x.count("falha crc")}\r\n')
                        if x.count("falha crc")>0:
                            corrompido = True
                        if not corrompido:
                            data = f'[{data[:len(data)-1]}]'
                            obj = json.loads(data)
                            apren = Aprendizado(node=Node.objects.get(id=int(obj[0]['node'])))
                            apren.save()
                            sleep(1)
                            contagem = 0
                            for x in obj:
                                if int(x['vibraX'])> apren.picoVibraX:
                                    apren.picoVibraX = int(x['vibraX'])
                                if int(x['vibraZ'])> apren.picoVibraZ:
                                    apren.picoVibraZ = int(x['vibraZ'])
                                if int(x['vibraX2'])> apren.picoVibraX2:
                                    apren.picoVibraX2 = int(x['vibraX2'])
                                if int(x['vibraZ2'])> apren.picoVibraZ2:
                                    apren.picoVibraZ2 = int(x['vibraZ2'])
                                if int(x['temp'])> apren.picoTemp:
                                    apren.picoTemp = int(x['temp'])
                                if int(x['corrente'])> apren.picoCorrente:
                                    apren.picoCorrente = int(x['corrente'])
                                log = AprendizadoLog(
                                    aprendizado=apren,
                                    time=datetime.strptime(x['time'],'%Y-%m-%d %H:%M:%S'),
                                    vibraX = int(x['vibraX']),
                                    vibraX2 = int(x['vibraX']),
                                    vibraZ = int(x['vibraZ']),
                                    vibraZ2 = int(x['vibraZ2']),
                                    temp = int(x['temp']),
                                    corrente = int(x['corrente']),
                                )
                                log.save()
                                contagem = contagem+1
                            index = contagem
                            mediaX = 0
                            mediaX2 = 0
                            mediaZ = 0
                            mediaZ2 = 0
                            mediaT = 0
                            mediaC = 0
                            vetor = AprendizadoLog.objects.filter(aprendizado=apren)
                            for n in vetor:
                                mediaX = n.vibraX+mediaX
                                mediaX2 = n.vibraX2+mediaX2
                                mediaZ = n.vibraZ+mediaZ
                                mediaZ2 = n.vibraZ2+mediaZ2
                                mediaT = n.temp+mediaT
                                mediaC = n.corrente+mediaC
                            apren.mediaVibraX = mediaX/index*(100+apren.limiarMedia)/100
                            apren.mediaVibraX2 = mediaX2/index*(100+apren.limiarMedia)/100
                            apren.mediaVibraZ = mediaZ/index*(100+apren.limiarMedia)/100
                            apren.mediaVibraZ2 = mediaZ2/index*(100+apren.limiarMedia)/100
                            apren.mediaTemp = mediaT/index*(100+apren.limiarMedia)/100
                            apren.mediaCorrente = mediaC/index*(100+apren.limiarMedia)/100
                            apren.picoVibraX = apren.picoVibraX*(100+apren.limiarPico)/100
                            apren.picoVibraX2 = apren.picoVibraX2*(100+apren.limiarPico)/100
                            apren.picoVibraZ = apren.picoVibraZ*(100+apren.limiarPico)/100
                            apren.picoVibraZ2 = apren.picoVibraZ2*(100+apren.limiarPico)/100
                            apren.picoTemp = apren.picoTemp*(100+apren.limiarPico)/100
                            apren.picoCorrente = apren.picoCorrente*(100+apren.limiarPico)/100
                            apren.save()
                            # agora vamos atualizar os limites do nodeSetup:
                            setup = NodeSetup.objects.get(node=apren.node)
                            setup.alertVibraX = apren.mediaVibraX
                            setup.alertVibraXNv2 = apren.picoVibraX
                            setup.alertVibraX2 = apren.mediaVibraX2
                            setup.alertVibraX2Nv2 = apren.picoVibraX2
                            setup.alertVibraZ = apren.mediaVibraZ
                            setup.alertVibraZNv2 = apren.picoVibraZ
                            setup.alertVibraZ2 = apren.mediaVibraZ2
                            setup.alertVibraZ2Nv2 = apren.picoVibraZ2
                            setup.alertTemp = apren.mediaTemp
                            setup.alertTempNv2 = apren.picoTemp
                            setup.alertCorrente = apren.mediaCorrente
                            setup.alertCorrenteNv2 = apren.picoCorrente
                            setup.save()
                            dxm.deleteFile("SbFile2.dat")
                            sleep(1)
                            while dxm.fileExist("SbFile2.dat"):
                                dxm.deleteFile("SbFile2.dat")
                                print("tentando novamente apagar LOG...")
                                sleep(5)
                            print("aprendeu!!!!!!!!!!!!")
            ip.configurarStatus = 0
            ip.configurar = False
            ip.online = True
            ip.save()
        except KeyboardInterrupt:
            controle = False
        except Exception as EX:
            ip = Gateway.objects.all()[0]
            ip.configurarStatus = 0
            ip.configurar = False
            ip.online = False
            ip.save()
            sleep(5)
            print(f"falha na leitura {str(EX)}")

th = Thread(target=leitura).start()
