TIM ='DGW0,000173'

Header = 'SARC  SQWTUGPXCICLDT21 R00000000600010'

TIM = TIM + ''.join([' ']*(50-len(TIM)))

Header = Header + ''.join([' ']*(80-len(Header)))

msje = '000124,002,HAL3270v1,EST:MUE/003,ONLINE/0005/0020/0004/OFF,BATCH/0008/0010/0004/OFF,MP34/ON'

respuesta_micro = '000695,001,HAL3270v1,EST:MUE/015,ONLINE/0008/0070/0008/OFF,BATCH/0002/0020/0002/OFF,MP34/OFF'

datos = msje.split(':')[1].split(',')
''' --- Comentarios 
largo de msje online on = 24, con off 25

largo de msje batch on = 23, con off 24

largo msje mp34 on, 7, con off 8
'''
class Tram_to_Socket:
    '''
    Inicializa las variables globales
    '''
    def __init__(self, delay='',online='',batch='',mp34=''):
        self.delay = delay
        self.online = online
        self.batch = batch
        self.mp34 = mp34
        
    def actualizar(self,msje):
        '''
        Separa los datos y crea los espacios para que el largo del mensaje
        de ida sea de largo siempre de 80, primero se debe actualizar y con
        este metodo y luego con el metodo director, recrea la trama de salida
        '''
        datos = msje.split(':')[1].split(',')
        self.delay = datos[0]
        self.online = self.gen_online(datos[1])
        self.batch = self.gen_batch(datos[2])
        self.mp34 = self.gen_mp34(datos[3])
    def Director(self):
        '''
        Genera la trama de salida luego de la actualizacion de los datos
        '''
        print '---> <000> ' + self.delay +' ' + self.online + ' ' + self.batch + ' ' + self.mp34 + '  '
        print len('---> <000> ' + self.delay +' ' + self.online + ' ' + self.batch + ' ' + self.mp34 + '  ')
        trama ='---> <000> ' + self.delay +' ' + self.online + ' ' + self.batch + ' ' + self.mp34 + '  '
        return trama
    def gen_online(self,online):
        '''
        Genera el espacio en blanco si hay un ON en la trama
        '''
        if len(online) == 24:
            online = online + ' '
        return online 
    
    def gen_batch(self,batch):
        '''
        Genera el espacio en blanco si hay un ON en la trama
        '''
        if len(batch) == 23:
            batch = batch + ' '
        return batch
                    
    def gen_mp34(self,mp34):
        '''
        Genera el espacio en blanco si hay un ON en la trama
        '''
        if len(mp34) == 7:
            mp34 = mp34 + ' '
        return mp34
        
    def get_delay(self):
        '''
        Retorna el dato del delay para el objeto socket
        '''
        return int(self.delay.split('/')[1])


if __name__ == '__main__':
    a = Tram_to_Socket()
    a.Director()
