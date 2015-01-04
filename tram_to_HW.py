""" Director:  genera trama a HW, controlando que datos van hacia ella
    Inicio : genera la trama inicial
    Act_botones : actualza el estado de los botones
    Actualizar diccionario: lee el diccionario y actualiza los datos """

dicc ={'batch': ('00001560', 'ERR', '178'),
 'fecha': ('20140412', '09:26:51'),
 'mp34': ('00000612', 'ERR', '254'),
 'nombre_proceso': 'CICLDA21',
 'online': ('00000289', 'OK ', '000'),
 't_rechazo': '010',
 't_respuesta': '000200'}

import datetime
import time
respuesta_micro = '695,001,HAL3270v1,EST:MUE/015,ONLINE/0008/0070/0008/OFF,BATCH/0002/0020/0002/OFF,MP34/OFF'

class Tram_to_Serial:

    def __init__(self):
        '''
        Crea las variables iniciales y guarda los header en variables 
        globales para su suso posterior
        '''
        self.dicc_estado = {}
        self.ctrl_trama = 1
        self.header = '001,HAL3270v1,'
        self.header_led = 'LED:'
        self.header_displays = 'D7S:'
        self.header_Lcd = 'LCD:'
        self.online_nproc, self.online_stat, self.online_coderr = '', '', ''
        self.batch_nproc, self.batch_stat, self.batch_coderr = '', '', ''
        self.mp34_nproc, self.mp34_stat, self.mp34_coderr = '', '', ''
        self.fecha = '00/00/0000'
        self.hora = '00:00:00'
        self.nombre_proceso = '.'*10
        self.t_respuesta = '000000'
        self.t_rechazo = '000'
        
        self.p_mp34 = '0'
        self.p_online = '0'
        self.p_batch = '0'
        self.tr = ''
        self.tps = ''
        self.status_lan = '1'
        self.inicializacion = True

        self.signal_salida = False
        self.trama_leds = ''
        self.time_tuple = ''
        self.time_contador = 0

        self.time = time 
    def Inicio(self):
        '''
        Trama inicial que permite inicializar las comunicaciones
        '''
        self.trama_leds = '001,HAL3270v1,LED:1,0,0,0,0,0,0'
        return '001,HAL3270v1,LED:1,0,0,0,0,0,0'
    
    def director_trama(self):
        '''
        Genera la trama principal, controla que trama se genera.
        '''
        
        print self.ctrl_trama
        if self.ctrl_trama == 1:
            print 'codigo trama1'
            trama = self.generar_leds()
        elif self.ctrl_trama == 2:
            print 'codigo trama2'
            trama = self.generar_Displays()
        elif self.ctrl_trama == 3:
            print 'codigo trama3'
            trama = self.generar_Lcds()
        return trama 
        
    def act_diccionario(self, dicc):
        '''
        Actualiza el estado actual de las variables a mostrar en el Hardware, se alimenta
        de la informacion proveniente de un diccionario que viene desde el socket
        '''
        self.dicc_estado = dicc
        
        self.batch_nproc, self.batch_stat, self.batch_coderr = dicc['batch']
        self.online_nproc, self.online_stat, self.online_coderr = dicc['online']
        self.mp34_nproc, self.mp34_stat, self.mp34_coderr = dicc['mp34']
        self.nombre_proceso = dicc['nombre_proceso'] + '   '
        self.fecha, self.hora = dicc['fecha']
        self.t_respuesta = dicc['t_respuesta'][1:6]
        self.t_rechazo = dicc['t_rechazo']
        self.batch_stat = self.to_logical(self.batch_stat)
        self.online_stat = self.to_logical(self.online_stat)
        self.mp34_stat = self.to_logical(self.mp34_stat)
        
        
        
    def act_botones(self, micro_to_arm):
        '''
        Actualiza el estado de los leds indicadores de encendido o apagado de los
        botones
        '''
        micro_to_arm = micro_to_arm.split(':')[1].split('/')
        if self.signal_salida:
            self.p_online = self.to_logical(micro_to_arm[5].split(',')[0])
            self.p_batch = self.to_logical(micro_to_arm[9].split(',')[0])
            p_mp34 = micro_to_arm[10][0:3]
            self.p_mp34 = self.to_logical(p_mp34)
            self.signal_salida = False

        print self.p_online, self.p_batch, self.p_mp34
        
    def generar_leds(self):
        '''
        Genera la trama de leds, concatenando los header mas el estado de todos
        los procesos.
        '''
        self.ctrl_trama = 2

        if self.dicc_estado:
            # genera trama de leds
            lista_led = [self.status_lan, self.p_online, self.online_stat,
                        self.p_batch, self.batch_stat, self.p_mp34,
                        self.mp34_stat]
            print lista_led
        else:
            if self.inicializacion:
                lista_led =['1','1',self.p_online,'1',self.p_batch,'1',self.p_mp34,'1','1']
                self.inicializacion = not(self.inicializacion)
            else:
                lista_led =['0','0',self.p_online,'0',self.p_batch,'0',self.p_mp34,'0','0']
                self.inicializacion = not(self.inicializacion)
        
        self.trama_leds = self.header + self.header_led + ','.join(lista_led)
        return self.trama_leds


    def generar_Displays(self):
        '''
        Genera la trama para los displays de 7 segmentos, se encarga de mostrar
        el codigo de error si hay un error
        '''

        list_disp = ['']*5
        if self.online_stat == '0':
            list_disp[0] = self.online_nproc
        else:
            list_disp[0] = '0'*(8-len(self.online_coderr)) + self.online_coderr

        if self.batch_stat == '0':
            list_disp[1] = self.batch_nproc 
        else:
            list_disp[1] = '0'*(8-len(self.batch_coderr)) + self.batch_coderr
            
        if self.mp34_stat == '0':
            list_disp[2] = self.mp34_nproc
        else:
            list_disp[2] = '0'*(8-len(self.mp34_coderr)) + self.mp34_coderr 

        list_disp[3] = self.t_respuesta
        list_disp[4] = self.t_rechazo
       
        trama = self.header + self.header_displays + ','.join(list_disp)
        
        print trama
        self.ctrl_trama = 3
        
         
        dicc = {'online':[self.online_stat, self.online_nproc, self.online_coderr],
                'batch':[self.batch_stat, self.batch_nproc, self.batch_coderr],
                'mp34':[self.mp34_stat, self.mp34_nproc, self.mp34_coderr],
                'etc':[self.t_respuesta, self.t_rechazo]}
        #return dicc
	return trama

    def generar_Lcds(self):
        '''
        trama por definir
        '''
        self.ctrl_trama = 1
        x = datetime.datetime.now()
        fecha = '/'.join([time.strftime('%d'), time.strftime('%m'),str(x.year)])
        hora = time.strftime('%H:%M:%S')
        trama = self.header + self.header_Lcd + fecha + ',' + hora + ',' + self.nombre_proceso
        self.time_contador += 1

        print trama
        return trama 
        
    def to_logical(self, status):
        if status[0:2] == 'ON':
            return '0'
        elif status == 'OFF':
            return '1'
        elif status == 'ERR':
            return '1'
        elif status == 'OK':
            return '0'
        elif status == 'OK ':
            return '0'

    def director_leds(self):
        self.signal_salida = True

    def cambiar_statuslan(self, status):
        self.status_lan = str(status)


if __name__ == '__main__':
    pass
