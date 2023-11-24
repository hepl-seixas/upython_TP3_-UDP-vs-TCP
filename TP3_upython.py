import network   #on importe la librairie network 
import usocket
import urequests, ujson #on importe les librairie pour le http 
from machine import Pin #on importe Pin de la librairie machine
import time

tcp_port  = 1882; #port tcp et udp
udp_port  = 1881;
server_ip = '192.168.74.246'; #adresse du serveur node red (donc adresse du pc)



led = Pin(2, Pin.OUT) #configuration de la LED en sortie

#Connexion au  WIFI

SSID = 'AndroidAP16E5'
PASSWORD = 'tqov9936'
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    print('Connecting to Wi-Fi...')
    wlan.connect(SSID, PASSWORD) #Connection au wifi electroProjectWifi
    while not wlan.isconnected():
        pass
print('Connected to Wi-Fi:', SSID)

#connecté au wi-fi

led.value(0)    #Allume la led

def TCP(data): #création d'une fonction envoyant des données avec le protocole TCP
    TCP_socket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM) #création d'un objet socket
    # socket.AF_INET indique qu'on utilise l'IPV4. socket.SOCK_STREAM indique qu'on utilise un socket TCP
    addr = usocket.getaddrinfo(server_ip, tcp_port)[0][-1] #création d'un tuple contenant l'adresse IP et la port TCP
    TCP_socket.connect(addr) #connexion au serveur node_red afin d'établir la connextion TCP
    TCP_socket.sendto(str(data).encode(), addr) #encodage des données en donné binaire  et envoie sur le serveur node_red
    TCP_socket.close()

def UDP(data): #création d'une fonction envoyant des données avec le protocole UDP
    UDP_socket = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
    # socket.AF_INET indique qu'on utilise l'IPV4. socket.SOCK_DGRAM indique qu'on utilise un socket UDP
    addr = usocket.getaddrinfo(server_ip, udp_port)[0][-1] #création d'un tuple contenant l'adresse IP et la port UDP
    UDP_socket.sendto(str(data).encode(), addr) #encodage des données en donné binaire  et envoie sur le serveur node_red
    UDP_socket.close()

data = 0

while True:
    led.value(0)  # Allume la LED pour indiquer l'envoi de données

    # Envoi des données sur la socket TCP
    try:
        TCP(data) 
    except Exception as e:
        print("Error sending TCP data:", e)

    # Envoi des données sur la socket UDP
    try:
        UDP(data)
    except Exception as e:
        print("Error sending UDP data:", e)
    led.value(1)
    time.sleep(0.001)  # Ajout d'un delay
    data += 1 #incrémente la donnée envoyé de 1