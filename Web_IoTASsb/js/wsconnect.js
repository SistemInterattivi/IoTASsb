/*
Module to manage the IoTA Swarm Scribble Bots
<!--* Marco Ercolani in data 01.02.2025 -->
<!--* A.A. 2024/25 -->
<!--* Corso Interaction Design -->
<!--* Percorso di Studi Nuove Tecnologie dell'Arte -->
<!--* Accademia di Belle Arti di Urbino -->
<!--* del server teseo.abaurbino.it -->
*/

        /*
        Definition of web socket connection string
        */
        const wshost = "teseo.abaurbino.it";
        const wsport = "11856";
  	    const socket = new WebSocket('wss://'+wshost+':'+wsport);
		const commandSsb = ["IoTALedOn", "IoTALedOff", "IoTAMotorForward", "IoTAMotorBackward","IoTAMotorStop"];
        /*
        Function object Used to construct commands that are sent and received by the server
        */
        function Command_proxy(s,r,f,c) { 
            this.sender = s;
            this.recipient = r;
            this.filter=f;
    	    this.command = c; 
    	
    	    this.commandToJson = function(){
    		    var strcommandjson = JSON.stringify(this);
    		    //console.log("Valore convertito in Json del Vertice " +strcommandjson);
    		    return strcommandjson;
            }

            this.jsonToCommand = function(str){
                var cmd = JSON.parse(str);
                return cmd;
            }
        }
	/*
	Event that define the first connection of websocket
	*/
	socket.addEventListener('open', function (event) {
		/*
		var nt= Date.now();
		var f = new eventIoTA("pong",2,"heartbit",0,0,0,0,0,0,nt,0,0,0,"#000000",0,0);
		*/
		var ssbCommand="heartbit";
		var f = makeEventIota(sessionUid,ssbCommand);
		console.log( ' Record iniziale '+ f.eventIoTAToJson());
        var cmd = new Command_proxy('client_web', 'client_socket','false',f.eventIoTAToJson());
		console.log("Spedizione: " +cmd.commandToJson() );
		socket.send(cmd.commandToJson());		
	});
	/*
	Event that manage the receive of a message from websocket
	*/
	socket.addEventListener('message', function (event) {
		// When a message arrives you have to manage the response
		console.log(event.data);
		var cp_t = new Command_proxy("sender","recipient",false,"command");
		var cp = cp_t.jsonToCommand(event.data);
		console.log(" Comando in arrivo : "+ cp.command);
		var ssbCommand="heartbit";
		var slc_t = makeEventIota(sessionUid,ssbCommand);
		var slc = slc_t.jsonToeventIoTA(cp.command);
		console.log(" Testo " + slc.name + " Value " + slc.value + " Category " + slc.category );
		/*
		Attention!!!
		Here you need to analyze the Event fields and manage the request
		*/
		cmdrcv = commandSsb.includes(slc.category);
		if ((slc.category == 'heartbit') || (cmdrcv)){
			console.log("Arriva qualcosa : "+slc.category);
			drawFormCloud(cp.recipient,slc);
		}
	});
	/*
	Function that manage the send of a message to websocket
	*/
	const contactServer = (msg) => {
	    	/*
	    	The module in this function sends the event by converting it to JSON format
        	*/
        	var interprete = "false"
        	var cmd = new Command_proxy('client_web', 'client_socket',interprete,msg);
	    	console.log("Spedizione -----> : " +cmd.commandToJson() );
	    	socket.send(cmd.commandToJson());
	}
	

