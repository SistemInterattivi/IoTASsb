########################################################################
### Filename    : proxy_iota_aba.py
### Description : Turn on Shapes from the web - module proxy event from/to the web and the client
### Author      :  Marco Ercolani in data 25.01.2025
### A.A. 2024/2025
### Corso di Interaction Design 
### Scuola Nuove Tecnologie dell'Arte
### Accademia di Belle Arti di Urbino
### modification: 2025-01-25
########################################################################

import websockets
import asyncio
import socket
import threading
import ssl
import json
import sys
import argparse
import logging
import queue
from eventiota import eventIoTA
from collections import deque
from threading import Condition

# command line parameter management
parser = argparse.ArgumentParser("Proxy IoTA ABA server --- run python3 proxy_iota_aba.py ")
parser.add_argument("--address", dest='address', help="An address of network (es. localhost)",required="True")
parser.add_argument("--port_client_socket", dest="port_client_socket" , help="A port for connection client socket of raspberry (es. 8182)", required=True, type=int)
parser.add_argument("--port_client_websocket", dest="port_client_websocket", help="A port for connection client HTML (es. 8183)",required=True, type=int)
parser.add_argument("--logging", dest="logging", help="insert \"console\" for logging  output in to console or name file if logging in  separated file ",required=True)
parser.add_argument("--archive_client", dest="archive_client", help="Enter \"Yes\" if you want to archive all Events that are sent from the Client",required=True)
parser.add_argument("--archive_web", dest="archive_web", help="Enter \"Yes\" if you want to archive all Events that are sent from the Web",required=True)
# parser args configuration
args = parser.parse_args()
#### 
#### Configuring log information
####
proxylog = logging.getLogger()
### 
### Output analysis
###
if args.logging == "console":
    handler = logging.StreamHandler(sys.stdout)
else:
    handler = logging.FileHandler(args.logging,mode='w')
proxylog.setLevel(logging.DEBUG)
handler.setLevel(logging.DEBUG)
## handler.getLogger('asyncio').setLevel(logging.WARNING)
## proxylog.getLogger('asyncio').setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
proxylog.addHandler(handler)
# Server data
HOSTSERVER = args.address
CLIENTPORT = args.port_client_socket
WEBSOCKETPORT = args.port_client_websocket
# Activation to variable of Archive
Client_Archive = args.archive_client
Web_Archive = args.archive_web

proxylog.info ("Il server run with address: " + HOSTSERVER + " port client socket: "+ str(CLIENTPORT) +  " port client websocket: "+ str(WEBSOCKETPORT) )
#
# SSL environment configuration
#
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# Generate with Lets Encrypt, chown to current user and 400 permissions
ssl_cert = "ssl/fullchain_iota.pem"
ssl_key = "ssl/privkey_iota.pem"
#
ssl_context.load_cert_chain(ssl_cert, keyfile=ssl_key)
#
# A set of connected ws clients
connected = set()
connectedThread = set()
# A set of connected Socket clients
connectedThreadSocket = set()
clientAddress = 0
####
#### Class that implements message queuing in both w_to_c and c_to_w directions
#### ------ it will be necessary to understand whether the queue must have synchronization characteristics
class Queue:
    #
    # Class constructor
    #
    def __init__(self):
        self._elements = deque()
    #
    # Inserts an item into the queue
    #
    def enqueue(self, element):
        try:
            print("Attention! An element is inserted")
            self._elements.append(element)
        except Exception as e:
            print("Warning! Problems inserting -->",e)

    #
    # extracts an item into the queue
    #
    def dequeue(self):
        try:
            print("Attention! An element is removed")
            return self._elements.popleft()
        except:
            return None
    #
    # extracts an item into the queue
    #
    def qsize(self):
        try:
            ##### print("Attention! The number of items is verified")
            return len(self._elements)
        except Exception as e:
            print("Warning! Problems checking items -->",e)
# Message queue definitions
# Archive of messages from web socket
w_archive=None
w_archive_condition = None
# Message queue definitions
# Archive of messages from client socket
c_archive=None
c_archive_condition = None
# Message queue definitions
# Messages from web socket to client socket
w_to_c=None
w_to_c_condition = None
# Messages from client socket to web socket
c_to_w=None
c_to_w_condition = None
####
#### Definition and constructions of message queues
####
w_to_c = Queue()
w_to_c_condition = Condition()
c_to_w = Queue()
c_to_w_condition = Condition()
w_archive=Queue()
w_archive_condition = Condition()
c_archive=Queue()
c_archive_condition = Condition()
####
#### Management of insert message in the queue 
####
def insertMsgInQueue(m, c, q):
    c.acquire() # acquire it
    q.enqueue(m)
    print("Insert element :" , q.qsize())
    c.notify()  # --- new! -------
    c.release() # release it
    return q

####
#### Management dequeue message of the queue 
#### 
def removeMsgFromQueue(c,q):
    m=None
    c.acquire() # acquire it
    if  q.qsize() == 0:
        m=None
        #### In this case you don't have to wait for the queue to fill up ---- c.wait() 
    else:
        m=q.dequeue()
    c.release() # release it
    return m
####
#### Display queue message 
#### 
def displayQueue(q,str):
    if q.qsize() != 0 :
        print("Elements in queue: ",str, " --> ", q.qsize())
    #### print(list(q.queue))



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
        command_proxy_tmp = json.loads(cs)
        command_proxy_obj=command_proxy(command_proxy_tmp["sender"],command_proxy_tmp["recipient"],command_proxy_tmp["filter"], command_proxy_tmp["command"])
        return(command_proxy_obj)
    #
    # Method that invert the value of filter
    #
    def invert_filter(self):
        self.filter = not self.filter
#
def findAnswer(msg):
    ans = ""
    if len(msg) > 14:
        ans = msg[0:6]+".."+ msg[len(msg)-5:len(msg)]
    else :
        ans = msg
    return ans
#
# Definition of the socket server main thread that receives messages from the socket client
#
class ClientThread(threading.Thread):
    global c_to_w
    global c_to_w_condition
    #
    # Class constructor
    #
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        proxylog.info("New connection added: "+ json.dumps(clientAddress))
    #
    # Class run 
    #    
    def run(self):
        ### Global variables define in the main program
        global c_to_w
        global c_to_w_condition
        global c_archive
        global c_archive_condition
        ###
        proxylog.info("Connection from : "+ json.dumps(clientAddress))
        ###
        while True:
            try:
                in_data = self.csocket.recv(8192)
                cpreceive = command_proxy.command_proxy_to_json_object(in_data.decode())
            except Exception as e:
                print("An error occurred in to receive msg from client: ", e)
            
            if cpreceive.command=='bye':
              break
            else:
                if cpreceive.filter == True :
                    
                    swc_answer = eventIoTA.eventIoTA_to_json_object(cpreceive.command)
                    swc_answer.name = findAnswer( swc_answer.name )
                    swc_answer.category = findAnswer( swc_answer.category )
                    cpreceive.invert_filter()
                    cpreceive.command = swc_answer.eventIoTA_to_json_string()
                    cpreceive.invert_filter()
                    proxylog.info ("Message from Client socket "+ cpreceive.command_proxy_to_json_string())
            #####
            ##### Insertion of messages coming from the Client Socket and directed to the web Client into the queue
            ##### 
            try:
                c_to_w = insertMsgInQueue(cpreceive,c_to_w_condition,c_to_w)
                displayQueue(c_to_w,"c_to_w")
                c_archive = insertMsgInQueue(cpreceive,c_archive_condition,c_archive)
                displayQueue(c_to_w,"c_archive")

            except Exception as e:
                print("An error occurred:", e)
            ###
            ###
            proxylog.info ("Answer Message from Client socket "+ cpreceive.command_proxy_to_json_string())
            self.csocket.send(bytes(cpreceive.command_proxy_to_json_string(),'UTF-8'))
        proxylog.info("Client at "+ json.dumps(clientAddress) + "disconnected...")
####
#### This Class reads a message from the message queue coming from the web client socket and forwarded to the client socket
#### 
class ConsumerClientThread(threading.Thread):
    global w_to_c
    global w_to_c_condition
    ####
    #### Una coda globale di client socket
    ####
    #
    # Class constructor
    #
    def __init__(self,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        proxylog.info("New connection added and New Consumer Client Created ")

    #
    # Class run 
    #  
    def run(self):
        global w_to_c
        global w_to_c_condition
        global c_archive
        global c_archive_condition
        global Client_Archive
     
        proxylog.info("Run Consumer Client  ")
        ### At first if the archive is active and the queue is not empty
        if (c_archive.qsize() != 0) and ( Client_Archive == "Yes" ):
            print("----- Sincronizzazione client - Server -------")
            tmp_events = None
            tmp_events_condition = None
            tmp_events = Queue()
            tmp_events_condition = Condition()
            eq = None
            ### All old messages need to be sent
            #####
            ##### Send all old events in the Client Archive at the new connection of Socket client
            #####
            while c_archive.qsize() != 0:
                eq = removeMsgFromQueue(c_archive_condition,c_archive)
                if eq != None:
                   sendmsg = ""
                   proxylog.info("Message from Archive of client socket : "+ eq.command_proxy_to_json_string())
                   self.csocket.send(bytes(eq.command_proxy_to_json_string(),'UTF-8'))
                   tmp_events = insertMsgInQueue(eq,tmp_events_condition,tmp_events)
            eq = None
            while tmp_events.qsize() != 0:
                eq = removeMsgFromQueue(tmp_events_condition,tmp_events)
                if eq != None:
                    c_archive = insertMsgInQueue(eq,c_archive_condition,c_archive)
            #####
            ##### End of the send of events in the Archive Socket Client
            #####
        while True:
            cpreceive = None
            #
            # It checks whether there are messages waiting in the queue
            # 
            cpreceive = removeMsgFromQueue(w_to_c_condition, w_to_c)
            # If the queue is empty cpreceive is null
            if cpreceive != None:
                proxylog.info("Received from web client and send to client : " + cpreceive.command_proxy_to_json_string())
                if cpreceive.filter == True :
                    
                    swc_answer = eventIoTA.eventIoTA_to_json_object(cpreceive.command)
                    swc_answer.name = findAnswer( swc_answer.name )
                    swc_answer.category = findAnswer( swc_answer.category )
                    cpreceive.invert_filter()
                    cpreceive.command = swc_answer.eventIoTA_to_json_string()
                    proxylog.info ("Message from Client socket after the change"+ cpreceive.command_proxy_to_json_string())
                #
                proxylog.info("Message from web client to send at all socket clients connected : "+ cpreceive.command_proxy_to_json_string())
                for cs in connectedThreadSocket:
                    cs.send(bytes(cpreceive.command_proxy_to_json_string(),'UTF-8'))

####
#### This Class server waits the messages from the Client socket 
#### 
class ClientServerThread(threading.Thread):
  #
  # Class run 
  #  
  #### List of all socket clients connected
  global connectedThreadSocket
  ###
  ### Execution of Thread
  ###
  def run(self):
    #### List of all socket clients connected
    global connectedThreadSocket
    ####
    proxylog.info("This is client server run!")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOSTSERVER, CLIENTPORT))
    proxylog.info("Server started")
    proxylog.info("Waiting for client request..")
    while True:
        server.listen(1)
        clientsock, clientAddress = server.accept()
        #
        # Executing the server class thread
        #
        newthread = ClientThread(clientAddress, clientsock)
        newthread.start()
        #
        # Executing the web client messages consumer class
        #
        consumernewthread = ConsumerClientThread(clientsock)
        connectedThreadSocket.add(clientsock)
        consumernewthread.start()

####
#### Definition and creation of the Server Socket Thread
####
client_server_thread = ClientServerThread()
client_server_thread.start()
####
#### This class reads a message from the message queue coming from the client socket which is forwarded to the web client socket
#### 
class ConsumerWebClientThread(threading.Thread):
    global c_to_w
    global c_to_w_condition
    global c_archive
    global c_archive_condition
    global Web_Archive 
    #
    # Class constructor
    #
    def __init__(self, webclientsocket):
        threading.Thread.__init__(self)
        self.wcsocket = webclientsocket
        proxylog.info("New connection added and New Consumer Web Client created ")
    #
    # Class run 
    # 
    def run(self):
        global c_to_w
        global c_to_w_condition
        global w_archive
        global w_archive_condition
        global Web_Archive
        ### At first if the archive is active and the queue is not empty
        if (c_archive.qsize() != 0) and ( Web_Archive == "Yes" ):
            tmp_events = None
            tmp_events_condition = None
            tmp_events = Queue()
            tmp_events_condition = Condition()
            eq = None
            #####
            ##### Send all old events in the Web Archive at the new connection of web client
            #####
            while w_archive.qsize() != 0:
                eq = removeMsgFromQueue(w_archive_condition,w_archive)
                if eq != None:
                   sendmsg = ""
                   proxylog.info("Message from Archive of client socket : "+ eq.command_proxy_to_json_string())
                   sendmsg = self.sendtoWebClient(eq.command_proxy_to_json_string())
                   asyncio.run(sendmsg)
                   tmp_events = insertMsgInQueue(eq,tmp_events_condition,tmp_events)
            eq = None
            while tmp_events.qsize() != 0:
                eq = removeMsgFromQueue(tmp_events_condition,tmp_events)
                if eq != None:
                    w_archive = insertMsgInQueue(eq,w_archive_condition,w_archive)
            #####
            ##### End of the send of events in the Archive Web
            #####
        proxylog.info("Run Consumer Web Client  ")
        while True:
            cpreceive = None
            #
            # It checks whether there are messages waiting in the queue
            # 
            cpreceive = removeMsgFromQueue(c_to_w_condition,c_to_w)
            if cpreceive != None:
                proxylog.info("Message received from client Socket to Web Client : " + cpreceive.command_proxy_to_json_string())
                if cpreceive.filter == True :
                    
                    swc_answer = eventIoTA.eventIoTA_to_json_object(cpreceive.command)
                    swc_answer.name = findAnswer( swc_answer.name )
                    swc_answer.category = findAnswer( swc_answer.category )
                    cpreceive.command = swc_answer.eventIoTA_to_json_string()
                    cpreceive.invert_filter()
                    proxylog.info ("Message from Client socket after the change"+ cpreceive.command_proxy_to_json_string())
                # create the custom coroutine
                sendmsg = self.sendtoWebClient(cpreceive.command_proxy_to_json_string())
                # run the coroutine in an asyncio program
                asyncio.run(sendmsg)
                for connt in connectedThread:
                    sendmsg = connt.sendtoWebClient(cpreceive.command_proxy_to_json_string())
                    asyncio.run(sendmsg)

    async def sendtoWebClient(self, msg):
        await  self.wcsocket.send(msg)
#
# The main websocket function for this server
#
async def server_ws_proxy(websocket, path):
    global w_to_c
    global w_to_c_condition
    global w_archive
    global w_archive_condition
    proxylog.info("A client just connected")
    # Store a copy of the connected client
    connected.add(websocket)
    ##
    ## Creation and execution of the consumer Web Client Thread
    ## 
    consumerwebnewthread = ConsumerWebClientThread(websocket)
    connectedThread.add(consumerwebnewthread)
    consumerwebnewthread.start()
    ###
    ### Cycle for receiving messages from the web page
    ###
    try:
        async for message in websocket:
                    cpreceive = command_proxy.command_proxy_to_json_object(message)  
                    proxylog.info("Received message from client: " + cpreceive.command_proxy_to_json_string())
                    #
                    # It checks whether there are messages waiting in the queue
                    # 
                    ##if cpreceive.filter == True :
                    if cpreceive.filter == "true" :
                        
                        swc_answer = eventIoTA.eventIoTA_to_json_object(cpreceive.command)
                        swc_answer.name = findAnswer( swc_answer.name )
                        swc_answer.category = findAnswer( swc_answer.category )
                        cpreceive.invert_filter()
                        cpreceive.command = swc_answer.eventIoTA_to_json_string()
                        proxylog.info ("Message from Client socket after the change"+ cpreceive.command_proxy_to_json_string())
                    #
                    # Insert the new msg in the queue for the client socket
                    # 
                    print (cpreceive)
                    w_to_c = insertMsgInQueue(cpreceive,w_to_c_condition,w_to_c)
                     #
                    # Insert the new msg in the queue archive for the  client socket
                    # 
                    w_archive = insertMsgInQueue(cpreceive,w_archive_condition,w_archive)
                    #
                    # Send a response to all connected clients except sender
                    #
                    displayQueue(w_to_c,"w_to_c")
                    for conn in connected:
                        if conn != websocket:
                            proxylog.info("Message from a different client : " + cpreceive.command_proxy_to_json_string())
                            await conn.send( cpreceive.command_proxy_to_json_string())
                        else:
                            ##        #####
                            ##        ##### Insertion of messages coming from the Client Socket and directed to the web Client into the queue
                            ##        ##### 
                            ##        
                            proxylog.info("Message coming from the same client : " + cpreceive.command_proxy_to_json_string())
                            ### await conn.send( cpreceive.command_proxy_to_json_string())   
            
    # Handle disconnecting clients 
    except websockets.exceptions.ConnectionClosed as e:
        proxylog.warning("A client just disconnected")
    finally:
        connected.remove(websocket)



# Start the web socket server
proxylog.info("WebSocket Server of address: "+ HOSTSERVER + " listening on Port: " + str(WEBSOCKETPORT))
start_server = websockets.serve(server_ws_proxy, HOSTSERVER, WEBSOCKETPORT, ssl=ssl_context)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
