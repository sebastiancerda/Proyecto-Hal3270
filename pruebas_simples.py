from Dicc_to_Serial import Dic_to_serial
from tram_to_HW import Tram_to_Serial, dicc
from tram_to_socket import Tram_to_Socket
import logging
import logging.handlers
import sys
from termcolor import colored
import time
import serial
from server_serial import SimSerial
import socket




LOG_FILENAME = "/tmp/myservice.log"
LOG_LEVEL = logging.INFO
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


generador_dicc = Dic_to_serial()
gen_tramasSerial = Tram_to_Serial()
gen_tramasocket = Tram_to_Socket()
trama_anterior = ''
contador = 0
salto_de_linea = '\r'
trama_nolan = '001,HAL3270v1,LED:0,0,0,0,0,0,0'

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




try:
    ser = SimSerial()
    #ser = serial.Serial('/dev/ttyxuart2')
    #ser.baudrate = 38400
    logger.info('Instancia de comunicaciones creada exitosamente')
except serial.SerialException, e:
    print 'no se puede abrir puerto serial'
    logger.warning('Imposible abrir tunel de comunicaciones con el Hardware')
    sys.exit(2)

status_lan = False

contador_delysocket = 0
trama_salida = gen_tramasSerial.Inicio()

while True:
    ser.write(trama_salida + salto_de_linea)
    time.sleep(1.0/3)
    n = ser.inWaiting()
    if n > 0:
        respuesta_Hal = ser.read(n)
        print colored(respuesta_Hal, 'red')
        logger.info('Empiezan las comunicaciones con el Hardware HAL3270')
        break


def parser_options():
    logger.info('Parseado de los archivos de configuraciones para el socket')
    while True:
        config_file = open('config_file.txt', 'r')
        lineas_config = config_file.readlines()
        host, port = lineas_config
        host = host.split(' ')
        port = port.split(' ')
        if len(host) == 2 and len(port) == 2:
            host = host[1].split('\n')[0]
            port = int(port[1])
            conx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conx.settimeout(5)
            try:
                conx.connect((host, port))
                logger.info('Comunicacion establecida')
                conx.close()
                return host, port
            except:
                logger.warning('timeout: server de comunicaciones muy lento')
                ser.write(trama_nolan + salto_de_linea)
                respuesta_Hal = ser.readline()
                conx.close()
        logger.info('Archivo de configuraciones no creado correctamente')
        time.sleep(5)

host, port = parser_options()
try:
    gen_tramasSerial.act_botones(respuesta_Hal)
    gen_tramasSerial.act_diccionario(dicc)
except IndexError:
    logger.warning('Error en trama con hardware HAL3270')

while True:
    try:
        trama_salida = gen_tramasSerial.director_trama()
        ser.write(trama_salida + salto_de_linea)
        respuesta_Hal = ser.readline()
        ### metodo para tram to socket
        gen_tramasSerial.act_botones(respuesta_Hal)
        print respuesta_Hal
        ### empieza metodo
        time.sleep(1.0/3)
        gen_tramasocket.actualizar(respuesta_Hal)
        delay = gen_tramasocket.get_delay() * 3
        contador_delysocket += 1
        print colored(contador_delysocket, 'red')
    except IndexError:
        print 'error en trama'
        logger.warning('Error en trama de comunicacion')
        logger.warning('Trama de respuesta de microcontrolador: ' + respuesta_Hal)
        logger.warning('Trama enviada al microcontrolador: ' + trama_salida)

    if contador_delysocket > delay:
        mensaje_socket_salida = gen_tramasocket.Director()
        try:
            contador_delysocket = 0
            conx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conx.settimeout(5)
            conx.connect((host, port))
            a = conx.recv(1024)
            print colored(a, 'blue')
            conx.send(mensaje_socket_salida)
            respuesta = conx.recv(1024)
            print colored(respuesta, 'yellow')
        except socket.error, e:
            print e
            conx.close()
            logger.warning('Conexion perdida, inicia reconfiguracion del puerto de comunicaciones')
            host, port = parser_options()
        finally:
            conx.close()

        try:
            dicc = generador_dicc.director_busqueda(respuesta)
            gen_tramasSerial.director_leds()
            gen_tramasSerial.act_diccionario(dicc)
        except IndexError:
            print 'error en trama'





