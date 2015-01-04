'''
    Server con threads 
'''
### Lista

lista = ['']*10 

lista[0] = '<--- <000> O/00000289/OK /000 B/00234560/ERR/153 M/00346232/ERR/213 F/20140412/14:26:13/CICLDA21/123456/010'

lista[1] = '<--- <000> O/00203289/ERR/411 B/00261560/ERR/163 M/00623512/ERR/242 F/20140412/05:46:41/CICLDA21/025300/020'

lista[2] = '<--- <000> O/00012289/OK /000 B/07471560/OK /178 M/00346612/ERR/464 F/20140412/19:23:24/CICLDA21/000200/030'

lista[3] = '<--- <000> O/00023489/OK /000 B/00345560/ERR/138 M/00324612/OK /254 F/20140412/12:25:34/CICLDA21/000300/040'

lista[4] = '<--- <000> O/00000629/ERR/624 B/00724560/ERR/363 M/00727412/ERR/744 F/20140412/15:27:56/CICLDA21/006300/100'

lista[5] = '<--- <000> O/00034569/OK /000 B/00761560/ERR/737 M/00045712/ERR/474 F/20140412/19:29:34/CICLDA21/000640/005'

lista[6] = '<--- <000> O/00034569/OK /000 B/00274560/OK /178 M/00056853/OK /254 F/20140412/13:12:56/CICLDA21/003450/013'

lista[7] = '<--- <000> O/00002429/OK /000 B/00741560/ERR/274 M/00086612/ERR/463 F/20140412/09:28:04/CICLDA21/000010/060'

lista[8] = '<--- <000> O/00003859/ERR/264 B/00747560/OK /178 M/00967812/ERR/283 F/20140412/13:49:50/CICLDA21/000201/034'

lista[9] = '<--- <000> O/12456789/OK /000 B/07451560/ERR/835 M/00043512/OK /254 F/20140412/19:56:34/CICLDA21/000223/015'



import socket
import sys
from random import randint
from thread import *
from termcolor import colored
 
HOST = ''   # Nombre simbolico localhost
PORT = 8888 # puerto arbitrario
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket creado'
 
#Enlaza el objeto socket con las direcciones entregadas
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Error al enlazar. Codigo de error : ' + str(msg[0]) + ' Mensaje ' + msg[1]
    sys.exit()
     
print 'Enlace creado'
 
#Iniciar escucha del server
s.listen(10)
print 'Socket escuchando puerto'

#Funcion para manejar las conecciones. Maneja la tarea
def clientthread(conn):
    #Manda un mensaje al cliente conectado.
    conn.send('Bienvenido al sebiserver,mande un mensaje y luego return \n') #send only takes string
    dato_anterior = ''
    #Loop infinito que no termina hasta que data es vacio.
    while True:
         
        #Recive desde el cliente
        data = conn.recv(1024)
        data = str(data)
        if not data:
            break

        if data == dato_anterior:
            pass
        else:
            print 'trama nueva:  ' + data
            dato_anterior = data
        print colored(len(data), 'yellow')
        random = randint(0,9)
        print colored(lista[random], 'red')
        conn.sendall(lista[random])
     
    #Si se sale del loop la coneccion se cierra
    conn.close()
 
#Para mantenerse hablando con el server
while 1:
    #Espera para aceptar una coneccion
    conn, addr = s.accept()
    print 'Conectado con : ' + addr[0] + ':' + str(addr[1])
    #Inicia una nueva tarea tomando el primer argumento ccomo el nombre de la funcion para correr
    #el segundo argumento es una tupla para la funcion
    start_new_thread(clientthread ,(conn,))
 
s.close()
