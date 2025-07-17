########################################################################
# Filename    : eventiota.py
# Project IoTA Swarm Scribble Bots
# Description : Activation Scribble Bot with input commands that arrive from Internet
# Author      : Marco Ercolani in data 01.02.2025
# A.A. 2024/2025
# Corso di Interaction Design 
# Scuola Nuove Tecnologie dell'Arte
# Accademia di Belle Arti di Urbino
# modification: 2024-12-18
########################################################################
import json
####
#### Class that reprocesses message from/to in json format
####
class eventIoTA():
    #
    # Class constructor
    #
    # call the object
    # eventIoTA(<name>,value>,<category>,<position_x>,<position_y>,<position_z>,<velocity>,<acceleration>,<pressure>,<time>,<distance>,<brightness>,vectorPoint>)
    #
    def __init__(self,n,d,c,x,y,z,v,a,p,t,l,b,i,rgb,tp,tr,vct):
        self.name = n
        self.value = d
        self.category = c
        self.position_x = x
        self.position_y = y
        self.position_z = z
        self.velocity = v
        self.acceleration  = a
        self.pressure = p
        self.time = t
        self.distance = l
        self.brightness = b
        self.intensity = i
        self.color = rgb
        self.temperature = tp
        self.transparency = tr
        self.vector = vct
    
    #
    # Method that translates a command from object to string
    #
    def eventIoTA_to_json_string(self):
        ## Bisogna implementare try/cach
        return json.dumps(self.__dict__)
    #
    # Method that translates a command from string to object
    #
    def eventIoTA_to_json_object(iota):
        ## Bisogna implementare try/cach
        print("Cosa arriva da proxy:")
        print(iota)
        iota_tmp = json.loads(iota)
        iota_obj=eventIoTA(iota_tmp["name"],iota_tmp["value"],iota_tmp["category"],iota_tmp["position_x"],iota_tmp["position_y"],iota_tmp["position_z"],iota_tmp["velocity"],iota_tmp["acceleration"],iota_tmp["pressure"],iota_tmp["time"],iota_tmp["distance"],iota_tmp["brightness"],iota_tmp["intensity"],iota_tmp["color"],iota_tmp["temperature"],iota_tmp["transparency"],iota_tmp["vector"])
        return(iota_obj)

