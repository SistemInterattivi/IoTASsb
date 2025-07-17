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
        Draw Circle in canvas
        */
        function drawCircle(c, x, y, r, transparency, color) {
            console.log("Draw a Circle color ", color);
            c.beginPath();
            c.globalAlpha = transparency;
            c.arc(x, y, r, 0, 2 * Math.PI);
            c.fillStyle = color;
            c.fill();
            c.stroke();
        }

        /*
        Draw Square in canvas
        */
        function drawSquare(c, x, y, r, transparency, color) {
            console.log("Draw a Square color ", color);
            c.beginPath();
            c.fillStyle = color;
            c.globalAlpha = transparency;
            c.fillRect(x, y, r, r);
            c.fill();
            c.stroke();
        }

        /*
        Draw Rhombus in canvas
        */
        function drawRhombus(c, x, y, r, transparency, color) {
            console.log("Draw a Rhombus color ", color);
            c.beginPath();
            c.moveTo(x, y);
            c.lineTo(x+r, y+r);
            c.lineTo(x+2*r, y);
            c.lineTo(x+r, y-r);
            c.fillStyle = color;
            c.globalAlpha = transparency;
            //c.fillRect(x, y, r, r);
            c.fill();
            c.stroke();
        }

        /*
        Draw Triangle in canvas
        */
        function drawTriangle(c, x, y, r, transparency, color) {
            console.log("Draw a Triangle color ", color);
            c.beginPath();
            c.moveTo(x, y);
            c.lineTo(x, y+r);
            c.lineTo(x+r, y+r);
            c.fillStyle = color;
            c.globalAlpha = transparency;
            c.fill();
            c.stroke();
        }

        /*
        Draw Rectangle in canvas
        */
        function drawRectangle(c, x, y, r, transparency, color) {
            console.log("Draw a Rectangle color ", color);
            c.beginPath();
            c.fillStyle = color;
            c.globalAlpha = transparency;
            c.fillRect(x, y, r, r+50);
            c.fill();
            c.stroke();
        }

        /*
        Draw Ellipse in canvas
        */
        function drawEllipse(c, x, y, r, transparency, color) {
            console.log("Draw a Ellipse color ", color);
            c.beginPath();
            c.fillStyle = color;
            c.globalAlpha = transparency;
            c.ellipse(x, y, r, r+50, Math.PI / 2, 0, 2 * Math.PI);
            c.fill();
            c.stroke();
        }

         /*
        Draw All figures Geometric in canvas
        */
        function drawCarousel(c, x, y, r, transparency, color) {
            console.log("Draw a Carousel color ", color);
            drawCircle(c,x,y,r,transparency,"green");
            drawRectangle(c,x+r,y,r,transparency,"purple");
            drawTriangle(c,x+(2*r),y,r,transparency,"blue");
            drawEllipse(c,x+(3*r),y,r,transparency,"purple");
            drawSquare(c,x+(4*r),y,r,transparency,"red");
        }
         /*
        Draw a clockwise Spiral
        */
        function drawSpiralClockwise(ctx, centerx, centery, innerRadius, outerRadius, turns=2, startAngle=0){
            ctx.save();
            ctx.translate(centerx, centery);
            ctx.rotate(startAngle);
            let r = innerRadius;
            let turns_ = Math.floor(turns*4)/4;
            let dr = (outerRadius - innerRadius)/turns_/4;
            let cx = 0, cy = 0; 
            let directionx = 0, directiony = -1;
            
            ctx.beginPath();
            let angle=0;
            for(; angle < turns_*2*Math.PI; angle += Math.PI/2){
                //draw a quarter arc around the center point (x, cy)
                console.log(cx+ " "+cy+ " " + angle + " " + turns_*2*Math.PI);
                ctx.arc( cx, cy, r, angle, angle + Math.PI/2);
                
                //move the center point and increase the radius so we can draw a bigger arc
                cx += directionx*dr;
                cy += directiony*dr;
                r+= dr;
                
                //rotate direction vector by 90 degrees
                [directionx, directiony] = [ - directiony, directionx ];
            }
            //draw the remainder of the last quarter turn
            ctx.arc( cx, cy, r, angle, angle + 2*Math.PI*( turns - turns_ ))
            ctx.stroke();
            ctx.restore();
        }
         /*
        Draw an anticlockwise Spiral
        */
        function drawSpiralAnticlockwise(ctx, centerx, centery, innerRadius, outerRadius, turns=2, startAngle=0){
            ctx.save();
            ctx.translate(centerx, centery);
            ctx.rotate(startAngle);
            let r = innerRadius;
            let turns_ = Math.floor(turns*4)/4;
            let dr = (outerRadius - innerRadius)/turns_/4;
            let cx = 0, cy = 0; 
            let directionx = 0, directiony = -1;
            console.log("qui");
            ctx.beginPath();
            let angle=0;
            for(; angle > -(turns_*2*Math.PI); angle -= Math.PI/2){
                //draw a quarter arc around the center point (x, cy)
                console.log(cx+ " "+cy+ " " + angle + " " + (-(turns_*2*Math.PI)));
                ctx.arc( cx, cy, r, angle, angle + Math.PI/2);
                
                //move the center point and increase the radius so we can draw a bigger arc
                cx += directionx*dr;
                cy += directiony*dr;
                r+= dr;
                
                //rotate direction vector by 90 degrees
                [directionx, directiony] = [ - directiony, directionx ];
            }
            //draw the remainder of the last quarter turn
            ctx.arc( cx, cy, r, angle, angle + 2*Math.PI*( turns - turns_ ))
            ctx.stroke();
            ctx.restore();
        }
        
        
