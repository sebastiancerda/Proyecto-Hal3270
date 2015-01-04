respuesta_micro = ['']*10

respuesta_micro[0] = '001,HAL3270v1,EST:MUE/015,ONLINE/0008/0070/0008/OFF,BATCH/0002/0020/0002/OFF,MP34/OFF'
respuesta_micro[1] = '002,HAL3270v1,EST:MUE/015,ONLINE/0008/0070/0008/OFF,BATCH/0002/0020/0002/OFF,MP34/OFF'
respuesta_micro[2] = '003,HAL3270v1,EST:MUE/015,ONLINE/0008/0070/0008/OFF,BATCH/0002/0020/0002/OFF,MP34/OFF'
respuesta_micro[3] = '004,HAL3270v1,EST:MUE/015,ONLINE/0008/0070/0008/OFF,BATCH/0002/0020/0002/OFF,MP34/OFF'
respuesta_micro[4] = '005,HAL3270v1,EST:MUE/015,ONLINE/0008/0070/0008/OFF,BATCH/0002/0020/0002/OFF,MP34/OFF'
respuesta_micro[5] = '006,HAL3270v1,EST:MUE/015,ONLINE/0008/0070/0008/OFF,BATCH/0002/0020/0002/OFF,MP34/OFF'
respuesta_micro[6] = '007,HAL3270v1,EST:MUE/015,ONLINE/0008/0070/0008/OFF,BATCH/0002/0020/0002/OFF,MP34/OFF'
respuesta_micro[7] = '008,HAL3270v1,EST:MUE/015,ONLINE/0008/0070/0008/OFF,BATCH/0002/0020/0002/OFF,MP34/OFF'
respuesta_micro[8] = '009,HAL3270v1,EST:MUE/015,ONLINE/0008/0070/0008/OFF,BATCH/0002/0020/0002/OFF,MP34/OFF'
respuesta_micro[9] = '010,HAL3270v1,EST:MUE/015,ONLINE/0008/0070/0008/OFF,BATCH/0002/0020/0002/OFF,MP34/OFF'

from random import randint

class SimSerial(object):

    def __init__(self):
        self.contador = 0
        self.indice = 0
        self.msj_respuesta = respuesta_micro

    def write(self, dato):
        print dato
        random = randint(0, 9)
        if random > 8:
            self.contador += 1
        if self.contador == 15:
            self.contador = 0
            self.indice = randint(0, 9)

    def readline(self):
        indice = int(self.indice)
        return self.msj_respuesta[indice]

    def baudrate(self, baud):
        return baud

    def Serial(self, puerto):
        return 'Server Serial iniciado' + puerto

    def inWaiting(self):
        return 2

    def read(self, arg):
        indice = int(self.indice)
        return self.msj_respuesta[indice]
if __name__ == '__main__':
    a = SimSerial()
