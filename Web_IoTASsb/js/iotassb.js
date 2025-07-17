/*
Module to manage the IoTA Swarm Scribble Bots
<!--* Marco Ercolani in data 01.02.2025 -->
<!--* A.A. 2024/25 -->
<!--* Corso Interaction Design -->
<!--* Percorso di Studi Nuove Tecnologie dell'Arte -->
<!--* Accademia di Belle Arti di Urbino -->
<!--* del server teseo.abaurbino.it -->
*/

var time_pressure = null;
var sessionUid = null;
var time_draw =  Date.now();
const MAXSIZE = 100;
const padding = 10;
var cx = padding;
var cy = padding;

/*
Function that make an eventIota 
*/
function makeEventIota(c_uid, c_ssb){
  var nt= Date.now();
  var wcolor ="#000000";
  var ssb_vct= [] ;
  var f = new eventIoTA("ssb"+c_uid,1,c_ssb,0,0,0,0,0,0,nt,0,0,0,wcolor,0,0,ssb_vct);
  console.log( ' Record iniziale '+ f.eventIoTAToJson());
  return f;
}
/*
Function that reset at zero the all time of pressure of button
*/
function reset_time(){
  time_pressure = null;
}
/*
Function entry point JQuery
*/
$( document ).ready(function() {
    console.log( "ready!" );
    //  Calculation of the fingerprint of device
    sessionUid=uid;
    console.log( "Fingerprint : " +uid);
    $("#ImgIoTASSBScreen").click(function(){
        saveAsPng();
    });
    //  When there is a click on the green icon, you need to draw a green circle on the board with the addRectCloud function with the color "Green"
    $("#ImgIoTASSBLedOn").click(function(){
          addSSBCloud("IoTALedOn");
    });
    $("#ImgIoTASSBLedOff").click(function(){
          addSSBCloud("IoTALedOff");
    });
    $("#ImgIoTASSBMotorForward").click(function(){
          addSSBCloud("IoTAMotorForward");
    });
    $("#ImgIoTASSBMotorBackward").click(function(){
          addSSBCloud("IoTAMotorBackward");
    });
    $("#ImgIoTASSBMotorStop").click(function(){
          addSSBCloud("IoTAMotorStop");
    });
    
    /*
    Attention!!
    you will need to insert the instructions for the other actions
    */
    
});

/*
Function used to add action to canvas in the page web and send this to server 
in the Ping Project
*/
function addSSBCloud(ssbCommand) {
    var np;
    // Preparing the Event to be sent to the IoTA Proxy
    np = makeEventIota(sessionUid, ssbCommand);
    // You draw the circle on the board
    drawFormCloud("client_web",np);
    // You send the event with the same color to IoTA Proxy
    contactServer(np.eventIoTAToJson());  
  }


/*
  Function that calculates random values ​​from min to max
*/
function randomCloudRadius(min, max,cx,cy,cwidth,cheight) {
    var r = 0 ;
    while (( r ==0 ) ||  ( r > cx ) || ( r > cy ) || ( r > (cwidth -cx))  ||  ( r > (cheight -cy)) ) {
        console.log(" Estremi ----  cx : ",cx , " cy : " , cy , " cw -cx : " , cwidth -cx , " ch -cy : " , cheight -cy ); 
        r = Math.round(min + Math.random() * (max - min));
    }
    return r ;
}
/*
  Function that calculates the new position of a coordinate. The new position depends from seconds of time
*/
function getNewPosition( c,s,l, m){
  var nc = 0;
  var npx= 0 ;
  nc = Math.round((s/60)*m); 
  if ( c+nc+l  > m ) {
     npx = padding ;
  } else {
     npx = c+nc;
  }
  return npx;
}
/*
Draw a Ping image into canvas
*/
function drawFormCloud(sender,np){
    var pingimage = new Image();
    var cnv = document.getElementById("cnvIoTASSB");
    
    if ( cnv != null ) {
        var cx = padding;
        var cy = padding;
        var lx = padding;
        // 
        var ctx = cnv.getContext("2d");
        var cwidth = ctx.canvas.width;
        var cheight = ctx.canvas.height;
        //
        //  it calculates the coordinates of circle with time
        //  
        var pingtime = new Date(np.time);
        var pingseconds = pingtime.getSeconds();
        cx = getNewPosition(cx, pingseconds,lx,cwidth);
        cy = getNewPosition(cy, pingseconds,lx,cheight);
        //  it calculates the radius
        lx = randomCloudRadius(1,MAXSIZE,cx,cy,cwidth,cheight);
        //
        console.log("Draw " +" Command "+ np.category + " Color " + np.color + " in position x: "+cx+" cy: "+cy + " con raggio: "+lx);
        
        // Single color
        switch (np.category) {
                case 'IoTALedOn':
                    drawCircle(ctx,cx,cy,lx,0.3,"#00FF00");
                break;
                case 'IoTALedOff':
                    drawCircle(ctx,cx,cy,lx,0.3,"#0000FF");
                break;
                case 'IoTAMotorForward':
                    drawSpiralClockwise(ctx, cx, cy, 10, 120, turns=10, startAngle=0);
                    //drawClockwiseSpiral(ctx,cx,cy,lx,0.4,"#00FF00");
                break;
                case 'IoTAMotorBackward':
                    drawSpiralAnticlockwise(ctx, cx, cy, 10, 120, turns=10, startAngle=0);
                    //drawAnticlockwiseSpiral(ctx,cx,cy,lx,0.4,"#FF0000");
                break;
                case 'IoTAMotorStop':
                    drawCircle(ctx,cx,cy,lx,0.3,"#0000FF");
                break;
                default:
                    console.log('Sorry, the command is wrong.');
        }
        
        
    }

}
/*
 Function that convert the Canvas to Image png
*/
function saveAsPng(){
    
    var canvas = document.getElementById("cnvIoTAPing");
    var image = new Image();
    var link = document.createElement("a");
    // Make a link
    image.src = canvas.toDataURL();
    link.href = image.src;
    link.download = "ping_cloud_image.png.png";
    // Execute the link
    link.click();

}

/*
  Function that send the value of like to DataBase
*/
function like(idprogetto, totprj) {

    sessionUid = "1323889";
    likeurl=  "https://teseo.abaurbino.it/sisteminterattivi/preferenze/preferenze.php";
    dataurl = "?idsession="+sessionUid+"&totprj="+totprj+"&idprogetto="+idprogetto;
    if (sessionUid == null) {
        document.getElementById("totLike").innerHTML = "Warning! Like system is not online";
        return;
    } else {
        var xmlhttp = new XMLHttpRequest();
        completeurl = likeurl+dataurl;
        xmlhttp.open("GET", completeurl , true);
        xmlhttp.send();
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                document.getElementById("totLike").innerHTML = xmlhttp.responseText; 
            }
        };
    }
}