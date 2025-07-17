########################################################################
# Filename    : client_IoTASsb.py
# Project IoTA Swarm Scribble Bots
# Description : Activation Scribble Bot with input commands that arrive from Internet
# Author      : Marco Ercolani in data 01.02.2025
# A.A. 2024/2025
# Corso di Interaction Design 
# Scuola Nuove Tecnologie dell'Arte
# Accademia di Belle Arti di Urbino
# modification: 2024-12-23
########################################################################
import socket
import threading
import sys
import argparse
import json
import logging
import time
import bluetooth
from eventiota import eventIoTA
from datetime import datetime
# 
# Configuring log information
proxylog = logging.getLogger()
proxylog.setLevel(logging.DEBUG)
####
#### In case you want to see the logs on console
#### handler = logging.StreamHandler(sys.stdout)
#### handler = logging.StreamHandler()
handler = logging.FileHandler("client_iotassb.log",mode='w')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
proxylog.addHandler(handler)
#
# command line parameter management
parser = argparse.ArgumentParser("Client Proxy IoTA ABA server --- run python3 client_proxy_iota_aba.py ")
parser.add_argument("--address", dest='address', help="An address of network (es. localhost)",required="True")
parser.add_argument("--port_client_socket", dest="port_client_socket" , help="A port for connection client socket of raspberry (es. 8182)", required=True, type=int)
#
# parser configuration
args = parser.parse_args()
# Server Network data
SERVER = args.address
PORT = args.port_client_socket
###
### List of the command Bot
###
listCommand = ['IoTALedOn','IoTALedOff','IoTAMotorForward','IoTAMotorBackward','IoTAMotorStop']
###
### Convert Events IoTA in Command Bot
###
def convertIoTAtoBot(cmdIoTA):
    ### Bluetooth Mac Address
    ### Warning! Every Esp32 has your Mac
    ### Example "D8:BC:38:E4:5E:2A"
    ###
    print("Comando verso il BOT ---->", cmdIoTA)
    target_address = "1C:69:20:CD:7B:DA"
    portBluetooth = 1
    success = 0
    if target_address is not None:
        print ("found target bluetooth device with address ", target_address)
        try:
            s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            s.connect((target_address,portBluetooth))
            data = cmdIoTA
            enddata=""
            print("Start send data")
            s.send(bytes(data, 'UTF-8'))
            print(data)
            s.send(bytes(enddata, 'UTF-8'))
            success = 1
        except:
            success = 0
            print("Server Bluetooth non disponible")
        s.close()
    else:
        print ("could not find target bluetooth device nearby")
    return success
##
## Preparing for the first Test Event
####
def makeEvent():
    vct =[]
    nt = time.time()
    slc = eventIoTA("ssbheartbeat",0,"heartbeat",0,0,0,0,0,0,nt,0,0,0,"#000000",0,0,vct)
    return slc
####
#### Producer class that prepares all data to be sent to the proxy server 
####
class ProducerClientThread(threading.Thread):
    #
    # Class constructor
    #
    def __init__(self,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        proxylog.info ("New connection added and New Producer Client created ")
    #
    # Class run 
    # 
    def run(self):
        proxylog.info  ("Run Producer Client ")
        msg = ''
        ####
        while True:
                f = False
                ###
                ### Make the object EventIoTA Ping
                ###
                slc = makeEvent()
                ###
                ### Make a command and Send the message
                ###
                cpsend = command_proxy('client_socket','client_web',f, slc.eventIoTA_to_json_string() )
                # convert into JSON string:
                sendmsg = cpsend.command_proxy_to_json_string()
                if sendmsg != None:
                    self.csocket.sendall(bytes(sendmsg,'UTF-8'))
                ###
                ### Wait ten seconds before sending again 
                ### 
                time.sleep(10)

####
#### Class that reprocesses proxy commands in json format
####
class command_proxy():
    #
    # Class constructor
    #
    def __init__(self,m,d,f,c):
        self.sender = m
        self.recipient = d
        self.filter = f
        self.command = c
    #
    # Method that translates a command from object to string
    #
    def command_proxy_to_json_string(self):
        return json.dumps(self.__dict__)
    #
    # Method that translates a command from string to object
    #
    def command_proxy_to_json_object(cs):
        try:
            command_proxy_tmp = json.loads(cs)
            command_proxy_obj=command_proxy(command_proxy_tmp["sender"],command_proxy_tmp["recipient"],command_proxy_tmp["filter"], command_proxy_tmp["command"])
        except:
            print("Warning! Message conversion error")
            proxylog.info ("Warning: Message conversion error")
            command_proxy_obj=command_proxy("dummy","dummy","false","dummy")
        #
        # Return value: the well-formatted command or the bad command warning
        return(command_proxy_obj)
    #
    # Method that invert the value of filter
    #
    def invert_filter(self):
        self.filter = not self.filter
####
#### Main program that receives and processes commands in json format
####
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
### Command with
### Make the object EventIoTA Ping
##
slc_c = makeEvent()
cpsend = command_proxy('client_socket','client_web',False, slc_c.eventIoTA_to_json_string() )
# convert into JSON string:
jmsg = cpsend.command_proxy_to_json_string()
client.sendall(bytes(jmsg,'UTF-8'))
producernewthread = ProducerClientThread(client)
producernewthread.start()
message=""
while True:
    in_data =  client.recv(8192)
    if in_data[-1] == 125:
        message=message+in_data.decode()
        cpreceive = command_proxy.command_proxy_to_json_object(message)
        message=""
        if cpreceive.sender == "dummy":
            print("Warning! Message broken")
            proxylog.info ("Warning! Message broken")
        else:
            proxylog.info ("From Server :" + cpreceive.command_proxy_to_json_string())
            if cpreceive.command=='bye':
                break
            else:
                ###
                ### Received a message from Server Proxy
                ###
                ssbmsg=cpreceive.command
                if cpreceive.sender=="client_web":
                    slc=eventIoTA.eventIoTA_to_json_object(ssbmsg)
                    print("Message received from  :",slc.name)
                    print("SSB with Color: ", slc.color)
                    ### Convert timestamp Javascript to Time Python 
                    pydate = datetime.fromtimestamp(int(slc.time / 1000.0))
                    print("SSB with Time: ",  pydate.strftime('%Y-%m-%d %H:%M:%S'))
                    print("SSB with Command ", slc.category)
                    if slc.category in listCommand:
                        ###
                        ### Enable incoming command SSB  from internet
                        ### 
                        ### Here you need to enter the actions to be performed when the event is received
                        ###
                        ### Run BOT
                        ###
                        success = convertIoTAtoBot(slc.category)
                        if success == 0:
                            necolor = "#FF0000"
                            print("Warning! Command failed :-((")
                        else:
                            necolor = "#00FF00"
                            print("Eureka! Command success! :-))")
                        ###
                        ### Send the response to client for the return command
                        ###
                        ne = makeEvent() 
                        ne.color = necolor
                        ne.value = success
                        ne.category = slc.category
                        nesend = command_proxy('client_socket','client_web',False, ne.eventIoTA_to_json_string() )
                         # convert into JSON string:
                        sendmsg = nesend.command_proxy_to_json_string()
                        if sendmsg != None:
                            try:
                                print(" Si spedisce il msg ---->", sendmsg)
                                client.sendall(bytes(sendmsg,'UTF-8'))
                            except:
                                print(" La spedizione non è andata bene ---->", sendmsg)
                    else:
                        print("Il comado non riconosciuto: ", slc.category)
                else:
                    print("Warning! Operation not recognized")
    else:
        message=message+in_data.decode()

client.close()



