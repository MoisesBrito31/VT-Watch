from django.db import models


class Estados(models.TextChoices):
    OK = '1'
    FALHA = '2'
    ALERTA = '3'
    DESCONHECIDO = '0'

class OS(models.Model):
    name = models.CharField("nome",max_length=100)
    description = models.CharField("Descrição",max_length=500)
    create_at = models.DateTimeField(auto_now_add=True)


class Gateway(models.Model):
    name = models.CharField("dispositivo", max_length=20)
    address = models.IntegerField("endereço",unique=True, default=1)
    port = models.CharField("porta", max_length=20, default="COM4")
    boudrate = models.IntegerField("BoudRate", default=19200)
    online = models.BooleanField("Online")
    configurar = models.BooleanField("Configrando", default=False)
    configurarStatus = models.IntegerField("status Configurar", default=0)
    configurarMsg = models.CharField("config msg", max_length=20, default="ok")
    aprender = models.BooleanField("Aprender", default=False)
    motorIndex = models.IntegerField("Motor alvo", default=0)

    class Meta:
        verbose_name="Gateway"
        verbose_name_plural="Gateways"

    def __str__(self):
        return f'{self.name} id {self.address}'

class Node(models.Model):
    name = models.CharField("Equipamento", max_length=20)
    vibraX = models.DecimalField("X Veloc RMS", default=0.000, decimal_places=3,max_digits=12)
    vibraZ = models.DecimalField("Z Veloc RMS", default=0.000, decimal_places=3,max_digits=12)
    vibraX2 = models.DecimalField("X Acele Pico", default=0.000, decimal_places=3,max_digits=12)
    vibraZ2 = models.DecimalField("Z Acele Pico", default=0.000, decimal_places=3,max_digits=12)
    corrente = models.DecimalField("Corrente", default=0.000, decimal_places=2,max_digits=12)
    temp = models.DecimalField("Temperatura", default=0.000, decimal_places=1,max_digits=12)
    estado = models.CharField("Estado",max_length=2,choices=Estados.choices,default=Estados.DESCONHECIDO)
    online = models.BooleanField("Online")
    alerta = models.CharField("alerta",max_length=30,default="000000")

    class Meta:
        verbose_name="Node"
        verbose_name_plural="Nodes"

    def __str__(self):
        return f'{self.name}'

class NodeSetup(models.Model):
    node = models.ForeignKey(Node,on_delete=models.CASCADE)
    nodeId = models.IntegerField("Node", default=1)
    address = models.IntegerField("endereço", default=1)
    ciclo = models.IntegerField("ciclo de logs (s)", default=60,)
    addrVibraX = models.IntegerField("endereço X Veloc RMS", default=1)
    addrVibraZ = models.IntegerField("endereço Z Veloc RMS", default=1)
    addrVibraX2 = models.IntegerField("endereço X Acele Pico", default=1)
    addrVibraZ2 = models.IntegerField("endereço Z Acele Pico", default=1)
    addrTemp = models.IntegerField("endereço Temperatura", default=1)
    addrCorrente = models.IntegerField("endereço Corrente", default=1)
    alertVibraX = models.DecimalField("Alert X Veloc - nv1", default=5.000, decimal_places=3,max_digits=12)
    alertVibraZ = models.DecimalField("Alert Z Veloc - nv1", default=5.000, decimal_places=3,max_digits=12)
    alertTemp = models.DecimalField("Alert Temperatura nv1", default=50.0, decimal_places=1,max_digits=12)
    alertCorrente = models.DecimalField("Alert Corrente nv1", default=10.0, decimal_places=2,max_digits=12)
    alertVibraXNv2 = models.DecimalField("Alert X Veloc - nv2", default=15.000, decimal_places=3,max_digits=12)
    alertVibraZNv2 = models.DecimalField("Alert Z Veloc - nv2", default=15.000, decimal_places=3,max_digits=12)
    alertTempNv2 = models.DecimalField("Alert Temperatura nv2", default=70.00, decimal_places=1,max_digits=12)
    alertVibraX2 = models.DecimalField("Alert X Acele - nv1", default=5.000, decimal_places=3,max_digits=12)
    alertVibraZ2 = models.DecimalField("Alert Z Acele - nv1", default=5.000, decimal_places=3,max_digits=12)
    alertVibraX2Nv2 = models.DecimalField("Alert X Acele - nv2", default=15.000, decimal_places=3,max_digits=12)
    alertVibraZ2Nv2 = models.DecimalField("Alert Z Acele - nv2", default=15.000, decimal_places=3,max_digits=12)
    alertCorrenteNv2 = models.DecimalField("Alert Corrente nv2", default=20.0, decimal_places=2,max_digits=12)
    fatorVibraX = models.IntegerField("fator X Veloc RMS", default=1000)
    fatorVibraZ = models.IntegerField("fator Z Veloc RMS", default=1000)
    fatorVibraX2 = models.IntegerField("fator X Acele Pico", default=1000)
    fatorVibraZ2 = models.IntegerField("fator Z Acele Pico", default=1000)
    fatorTemp = models.IntegerField("fator Temperatura", default=100)
    fatorCorrente = models.IntegerField("fator Corrente", default=1)
    aprenderTime= models.IntegerField("qtds de medicoes para Aprender", default=10)
    aprenderCiclo= models.IntegerField("tempo entre medicoes p/ Apdr", default=60)

    class Meta:
        verbose_name="NodeSetup"
        verbose_name_plural="NodeSetups"

    def __str__(self):
        return f'setup do node: {self.node}'


class Hist(models.Model):
    time = models.DateTimeField('Data')
    node = models.ForeignKey(Node,on_delete=models.CASCADE)
    alertVibraX = models.DecimalField("Alert X Veloc - nv1", default=5.000, decimal_places=3,max_digits=12)
    alertVibraZ = models.DecimalField("Alert Z Veloc - nv1", default=5.000, decimal_places=3,max_digits=12)
    alertTemp = models.DecimalField("Alert Temperatura nv1", default=50.0, decimal_places=1,max_digits=12)
    alertCorrente = models.DecimalField("Alert Corrente nv1", default=10.0, decimal_places=2,max_digits=12)
    alertVibraXNv2 = models.DecimalField("Alert X Veloc - nv2", default=15.000, decimal_places=3,max_digits=12)
    alertVibraZNv2 = models.DecimalField("Alert Z Veloc - nv2", default=15.000, decimal_places=3,max_digits=12)
    alertTempNv2 = models.DecimalField("Alert Temperatura nv2", default=70.00, decimal_places=1,max_digits=12)
    alertVibraX2 = models.DecimalField("Alert X Acele - nv1", default=5.000, decimal_places=3,max_digits=12)
    alertVibraZ2 = models.DecimalField("Alert Z Acele - nv1", default=5.000, decimal_places=3,max_digits=12)
    alertVibraX2Nv2 = models.DecimalField("Alert X Acele - nv2", default=15.000, decimal_places=3,max_digits=12)
    alertVibraZ2Nv2 = models.DecimalField("Alert Z Acele - nv2", default=15.000, decimal_places=3,max_digits=12)
    alertCorrenteNv2 = models.DecimalField("Alert Corrente nv2", default=20.0, decimal_places=2,max_digits=12)
    vibraX = models.DecimalField("X Veloc RMS", default=0.000, decimal_places=3,max_digits=12)
    vibraZ = models.DecimalField("Z Veloc RMS", default=0.000, decimal_places=3,max_digits=12)
    vibraX2 = models.DecimalField("X Acele Pico", default=0.000, decimal_places=3,max_digits=12)
    vibraZ2 = models.DecimalField("Z Acele Pico", default=0.000, decimal_places=3,max_digits=12)
    temp = models.DecimalField("Temperatura", default=0.000, decimal_places=1,max_digits=12)
    corrente = models.DecimalField("Corrente", default=0.000, decimal_places=2,max_digits=12)

    class Meta:
        verbose_name="Registro"
        verbose_name_plural="Registros"

    def __str__(self):
        return f'Registro de {self.time}'

class Evento(models.Model):
    date = models.DateTimeField('Data',auto_now_add=True)
    node = models.ForeignKey(Node,on_delete=models.CASCADE)
    descricao = models.CharField('Evento',max_length=50,default="generico")
    tipo = models.CharField('tipo de Evento',max_length=50,default="Evento")

    class Meta:
        verbose_name="Evento"
        verbose_name_plural="Eventos"

    def __str__(self):
        return f'Evento de {self.descricao}'
    

class Aprendizado(models.Model):
    criado = models.DateTimeField(auto_now_add=True)
    node = models.ForeignKey(Node,on_delete=models.CASCADE)
    limiarPico = models.DecimalField("limiar para pico %", default=5,decimal_places=3,max_digits=12)
    limiarMedia = models.DecimalField("limiar para media %", default=2,decimal_places=3,max_digits=12)
    picoVibraX = models.DecimalField("Pico X RMS", default=0,decimal_places=3,max_digits=12)
    mediaVibraX = models.DecimalField("Media X RMS", default=0,decimal_places=3,max_digits=12)
    picoVibraX2 = models.DecimalField("Pico X Pico", default=0,decimal_places=3,max_digits=12)
    mediaVibraX2 = models.DecimalField("Media X Pico", default=0,decimal_places=3,max_digits=12)
    picoVibraZ = models.DecimalField("Pico Z RMS", default=0,decimal_places=3,max_digits=12)
    mediaVibraZ = models.DecimalField("Media Z RMS", default=0,decimal_places=3,max_digits=12)
    picoVibraZ2 = models.DecimalField("Pico Z Pico", default=0,decimal_places=3,max_digits=12)
    mediaVibraZ2 = models.DecimalField("Media Z Pico", default=0,decimal_places=3,max_digits=12)
    picoTemp = models.DecimalField("Pico T", default=0,decimal_places=3,max_digits=12)
    mediaTemp = models.DecimalField("Media T", default=0,decimal_places=3,max_digits=12)
    picoCorrente = models.DecimalField("Pico Corrente", default=0,decimal_places=3,max_digits=12)
    mediaCorrente = models.DecimalField("Media Corrente", default=0,decimal_places=3,max_digits=12)


class AprendizadoLog(models.Model):
    time = models.DateTimeField('Data')
    aprendizado = models.ForeignKey(Aprendizado,on_delete=models.CASCADE)
    vibraX = models.DecimalField("X Veloc RMS", default=0.000, decimal_places=3,max_digits=12)
    vibraZ = models.DecimalField("Z Veloc RMS", default=0.000, decimal_places=3,max_digits=12)
    vibraX2 = models.DecimalField("X Acele Pico", default=0.000, decimal_places=3,max_digits=12)
    vibraZ2 = models.DecimalField("Z Acele Pico", default=0.000, decimal_places=3,max_digits=12)
    temp = models.DecimalField("Temperatura", default=0.000, decimal_places=1,max_digits=12)
    corrente = models.DecimalField("Corrente", default=0.000, decimal_places=2,max_digits=12)


    