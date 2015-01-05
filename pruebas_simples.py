#!/usr/bin/env python

from Dicc_to_Serial import Dic_to_serial
from tram_to_HW import Tram_to_Serial, dicc
from tram_to_socket import Tram_to_Socket
import logging

import sys
from termcolor import colored
import time
import serial
from server_serial import SimSerial
import socket

logging.basicConfig(filename = 'events.log', format = '%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

logging.warning('Logger iniciado')

generador_dicc = Dic_to_serial()
gen_tramasSerial = Tram_to_Serial()
gen_tramasocket = Tram_to_Socket()
trama_anterior = ''
contador = 0
salto_de_linea = '\r'
trama_nolan = '001,HAL3270v1,LED:0,0,0,0,0,0,0'

try:
    ser = SimSerial()
    #ser = serial.Serial('/dev/ttyxuart2')
    #ser.baudrate = 38400
    logging.info('Creada instancia de comunicacion con el Hardware')
except serial.SerialException, e:
    logging.warning('Error critico, no se puede conectar al Hardware')
    logging.warning(e)
    sys.exit(2)


contador_delysocket = 0
contador_parser_options = 45
trama_salida = gen_tramasSerial.Inicio()

while True:
    ser.write(trama_salida + salto_de_linea)
    time.sleep(1.0/3)
    n = ser.inWaiting()
    if n > 0:
        respuesta_Hal = ser.read(n)
        print colored(respuesta_Hal, 'red')
        logging.info('Empiezan las comunicaciones con el Hardware HAL3270')
        break


def parser_options():
    logging.info('Parseado de los archivos de configuraciones para el socket')

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
            logging.info('Comunicacion establecida')
            conx.close()
            return host, port
        except socket.error, e:
            logging.warning('Imposible establecer comunicaciones con el server')
            logging.warning(e)
            conx.close()

    else:
        logging.info('Archivo de configuraciones no creado correctamente')

host, port = parser_options()
try:
    gen_tramasSerial.act_botones(respuesta_Hal)
    gen_tramasSerial.act_diccionario(dicc)
except IndexError:
    logging.warning('Error en trama proveniente del Hardware')
    logging.warning(respuesta_Hal)


dato_anterior = ''

while True:
    try:
        trama_salida = gen_tramasSerial.director_trama()
        ser.write(trama_salida + salto_de_linea)
        respuesta_Hal = ser.readline()

        if respuesta_Hal == dato_anterior:
            pass
        else:
            logging.info('Evento Hardware: ' + respuesta_Hal)
            dato_anterior = respuesta_Hal

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
        logging.warning('Error en trama de comunicacion')
        logging.warning('Trama de respuesta de microcontrolador: ' + respuesta_Hal)
        logging.warning('Trama enviada al microcontrolador: ' + trama_salida)

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
            gen_tramasSerial.cambiar_statuslan(1)
            gen_tramasSerial.director_leds()

        except socket.error, e:
            print e
            conx.close()
            gen_tramasSerial.cambiar_statuslan(0)
            logging.warning('Conexion perdida, inicia reconfiguracion del puerto de comunicaciones')
            logging.warning(e)

        finally:
            conx.close()

        try:
            dicc = generador_dicc.director_busqueda(respuesta)
            gen_tramasSerial.act_diccionario(dicc)
        except IndexError:
            logging.warning('Error en trama proveniente desde el socket')
            logging.warning(respuesta)
        except NameError:
            logging.warning('No hay mensaje de respuesta por el socket')
            print colored('Aun no se conecta al socket', 'red')
        except ValueError:
            logging.warning('Error en trama proveniente desde el socket')
            logging.warning(respuesta)

    if gen_tramasSerial.status_lan == 0:

        if contador_parser_options == 45:
            host, port = parser_options()
        if contador_parser_options == 0:
            contador_parser_options = 45
        contador_parser_options -= 1

