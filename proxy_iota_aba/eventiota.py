########################################################################
### Filename    : eventiota.py
### Description : Turn on Shapes from the web - module object event from the web
### Author      :  Marco Ercolani in data 25.01.2025
### A.A. 2024/2025
### Corso di Interaction Design 
### Scuola Nuove Tecnologie dell'Arte
### Accademia di Belle Arti di Urbino
### modification: 2025-01-25
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
    # eventIoTA(<name>,value>,<category>,<position_x>,<position_y>,<position_z>,<velocity>,<acceleration>,<pressure>,<time>,<distance>,<brightness>)
    #
    def __init__(self,n,d,c,x,y,z,v,a,p,t,l,b,i,rgb,tp,tr):
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
        
    #
    # Method that translates a command from object to string
    #
    def eventIoTA_to_json_string(self):
        strevent = ""
        try:
            strevent = json.dumps(self.__dict__)
        except:
            strevent = "{error:0}"
        
        return strevent
    #
    # Method that translates a command from string to object
    #
    def eventIoTA_to_json_object(iota):
        iota_obj=None
        try: 
            iota_tmp = json.loads(iota)
            iota_obj=eventIoTA(iota_tmp["name"],iota_tmp["value"],iota_tmp["category"],iota_tmp["position_x"],iota_tmp["position_y"],iota_tmp["position_z"],iota_tmp["velocity"],iota_tmp["acceleration"],iota_tmp["pressure"],iota_tmp["time"],iota_tmp["distance"],iota_tmp["brightness"],iota_tmp["intensity"],iota_tmp["color"],iota_tmp["temperature"],iota_tmp["transparency"])
        except:
            print("An exception ot occurred")
        
        return(iota_obj)

