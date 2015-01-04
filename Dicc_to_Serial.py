llegada = 'DGW0  UG1CDCV0         L00000000730003                                         ' \
          ' <--- <000> O/0000200/OK /000 B/0001560/OK /000 T/005/R/00270/F/20140728 182654'

datos = '<--- <000> O/00000289/OK /000 B/00001560/ERR/178 M/00000612/ERR/254 F/20140412/09:26:51/CICLDA21/000200/010'
datos_conerr = '<--- <123> O/00000289/ERR/000 B/00001560/ERR/178 M/00000612' \
               '/ERR/254 F/20140412/09:26:51/CICLDA21/000200/010'
import datetime
class Dic_to_serial:
    def __init__(self):
        '''
        Incializa las variables, guarda la posicion predeterminada
        para la el tiempo de respuesta, proceso y tasa de rechazo en 
        la trama
        '''
        self.dicc = {}
        self.pos_proc = 83
        self.t_respuesta = 92
        self.rechazo = 99
        self.hoy = 0

    def director_busqueda(self, trama):
        '''
        Luego de separar con split, busca la posicion de la O
        B,M y F para separar la distinta informacion de la trama
        tipo mostrada en datos.
        '''

	self.dato = trama.split('<--- ')[1]
	print self.dato
        codd = self.dato.split('>')[0]
        self.pos_o = self.dato.find('O')
        self.pos_b = self.dato.find('B')
        self.pos_m = self.dato.find('M')
        self.pos_f = self.dato.find('F')
        self.buscar_online()
        self.buscar_batch()
        self.buscar_mp34()
        self.buscar_fecha()
        self.buscar_nomproc()
        self.buscar_trespuesta()
        self.buscar_rechazo()

        codd_err = codd.split('<')[1]
        print 'codigo de error es' + codd_err
        if codd_err == '000':
            print self.dicc 
            return self.dicc
        else:
            self.dicc['online'] = ('0'*5 + codd_err, 'ERR', codd_err)
            self.dicc['batch'] = ('0'*5 + codd_err, 'ERR', codd_err)
            self.dicc['mp34'] = ('0'*5 + codd_err, 'ERR', codd_err)
            return self.dicc

    def buscar_online(self):
        '''
        Genera la llave de diccionario para online
        '''
        online = self.dato[self.pos_o:self.pos_b].split('/')
        print 'online es: ',  online
        self.dicc['online'] = (online[1], online[2], online[3][0:3])
        

    def buscar_batch(self):
        '''
        Genera la llave de diccionario para batch
        '''
        batch = self.dato[self.pos_b:self.pos_m].split('/')
        print 'batch es: ' , batch
        self.dicc['batch'] = (batch[1],batch[2],batch[3][0:3])
    
    def buscar_mp34(self):
        '''
        Genera la llave de diccionario para mp34
        '''
        mp34 = self.dato[self.pos_m:self.pos_f].split('/')
        print 'mp34 es: ' , mp34
        self.dicc['mp34'] = (mp34[1],mp34[2],mp34[3][0:3])

    def buscar_fecha(self):
        '''
        Genera la llave de diccionario para fecha
        '''
        fecha = self.dato[self.pos_f:84].split('/')
        print 'la fecha es : ',fecha

        self.dicc['fecha'] = (fecha[1], fecha[2])
        calendario, hora = self.dicc['fecha']
        ano = calendario[0:4]
        mes = calendario[4:6]
        dia = calendario[6:8]
        hora, minuto, segundo = hora.split(':')
        if not(self.hoy == int(dia)):
            tuple = (int(ano), int(mes), int(dia), int(hora), int(minuto), int(segundo), 0)
            self.actualizar_hora(tuple)
            self.hoy = int(dia)


    def buscar_nomproc(self):
        '''
        Genera la llave de diccionario para encontrar el nombre del proceso
        '''
        proce = self.dato[self.pos_proc:self.t_respuesta].split('/')
        print 'nombre de proceso :' , proce
        self.dicc['nombre_proceso'] = (proce[0])

    def buscar_trespuesta(self):
        '''
        Genera la llave de diccionario para encontrar t_respuesta
        '''
        t_respuesta = self.dato[self.t_respuesta:self.rechazo].split('/')
        print 'tiempo de respuesta :' , t_respuesta
        self.dicc['t_respuesta'] = t_respuesta[0]
    
    def buscar_rechazo(self):
        '''
        Genera la llave de diccionario para la taza de rechazo
        '''
        rechazo = self.dato[self.rechazo:102]
        print 'tasa de rechazo: ',rechazo
        self.dicc['t_rechazo'] = rechazo

    def actualizar_hora(self, time_tuple):
        import ctypes
        import ctypes.util
        import time

        # /usr/include/linux/time.h:
        #
        # define CLOCK_REALTIME                     0
        CLOCK_REALTIME = 0

        # /usr/include/time.h
        #
        # struct timespec
        #  {
        #    __time_t tv_sec;            /* Seconds.  */
        #    long int tv_nsec;           /* Nanoseconds.  */
        #  };
        class timespec(ctypes.Structure):
            _fields_ = [("tv_sec", ctypes.c_long),
                        ("tv_nsec", ctypes.c_long)]

        librt = ctypes.CDLL(ctypes.util.find_library("rt"))

        ts = timespec()
        ts.tv_sec = int(time.mktime(datetime.datetime(*time_tuple[:6]).timetuple() ) )
        ts.tv_nsec = time_tuple[6] * 1000000  # Millisecond to nanosecond

        # http://linux.die.net/man/3/clock_settime
        librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))

if __name__ == '__main__':
    obj = Dic_to_serial(datos)
    obj.director_busqueda()
