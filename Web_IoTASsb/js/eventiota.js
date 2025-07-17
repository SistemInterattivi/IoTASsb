/*
Module to manage the IoTA Swarm Scribble Bots
<!--* Marco Ercolani in data_ 01.02.2025 -->
<!--* A.A. 2024/25 -->
<!--* Corso Interaction Design -->
<!--* Percorso di Studi Nuove Tecnologie dell'Arte -->
<!--* Accademia di Belle Arti di Urbino -->
<!--* del server teseo.abaurbino.it -->
*/

/*
Function object Used to construct single record word that are sent and received by the server
*/
function eventIoTA(n,d,c,x,y,z,v,a,p,t,l,b,i,rgb,tp,tr,vct) { 
        this.name = n;
        this.value = d;
        this.category = c;
        this.position_x = x;
        this.position_y = y;
        this.position_z = z;
        this.velocity = v;
        this.acceleration  = a;
        this.pressure = p;
        this.time = t;
        this.distance = l;
        this.brightness = b;
        this.intensity = i; 
        this.color = rgb
        this.temperature = tp
        this.transparency = tr
        this.vector = vct;
    	// Class Method to transform EventIoTA to String Json
    	this.eventIoTAToJson = function(){
    		    var strcommandjson = JSON.stringify(this);
    		    //console.log("Valore convertito in Json del Vertice " +strcommandjson);
    		    return strcommandjson;
        }
        // Class Method to transform string Json to  EventIoTA
        this.jsonToeventIoTA = function(str){
                var cmd = JSON.parse(str);
                return cmd;
        }
}
