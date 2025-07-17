/*
Module to manage the IoTA Ping
<!--* Marco Ercolani in data_ 01.02.2025 -->
<!--* A.A. 2024/25 -->
<!--* Corso Interaction Design -->
<!--* Percorso di Studi Nuove Tecnologie dell'Arte -->
<!--* Accademia di Belle Arti  di Urbino -->
<!--* del server ercole.abaurbino.it -->
*/
/*
Funzione oggetto 
RandomColorRGB per generare un colore Randomico
Convertire da RGB to number e viceversa

Object function
RandomColorRGB to generate a Random color
Convert from RGB to number and vice versa

*/

function RandomColorRGB() {
    
	this.max = 255;
        
	this.randomInteger = function(max) {
    	return Math.floor(Math.random()*(max + 1));
	}
  
	this.randomRgbColor = function() {
    	let r = this.randomInteger(this.max);
    	let g = this.randomInteger(this.max);
    	let b = this.randomInteger(this.max);
    	return [r,g,b];
	}
    
	this.randomHexColor = function() {
    	let [r,g,b] = this.randomRgbColor();
 		//
    	let hr = r.toString(16).padStart(2, '0');
    	let hg = g.toString(16).padStart(2, '0');
    	let hb = b.toString(16).padStart(2, '0');
 		//
    	return "#" + hr + hg + hb;
	}
    // convert three r,g,b integers (each 0-255) to a single decimal integer (something between 0 and ~16m)
	this.colorToNumber = function(r, g, b) {
		return (r << 16) + (g << 8) + (b);
	}
	// convert it back again (to a string)
	this.numberToColor = function(number) {

		const r = (number & 0xff0000) >> 16;
		const g = (number & 0x00ff00) >> 8;
		const b = (number & 0x0000ff);
		
		return [r, g, b];
		// or eg. return `rgb(${r},${g},${b})`;
	}
	// convert the bumber into Hex RGB color
	this.numberToColor = function(number) {

		const r = (number & 0xff0000) >> 16;
		const g = (number & 0x00ff00) >> 8;
		const b = (number & 0x0000ff);
		
		let hr = r.toString(16).padStart(2, '0');
    	let hg = g.toString(16).padStart(2, '0');
    	let hb = b.toString(16).padStart(2, '0');
 		//
    	return "#" + hr.toUpperCase() + hg.toUpperCase() + hb.toUpperCase();
	} 
	// Hex RGB to Decimal RGB
	this.hextodecimalRGB = function(sHexRGB) {
		let r = sHexRGB.substr(1, 2);
		let g = sHexRGB.substr(3, 2);
		let b = sHexRGB.substr(5, 2);
		let decr = parseInt(r, 16);
		let decg = parseInt(g, 16);
		let decb = parseInt(b, 16);
		return [decr,decg,decb];
	}
}

function getColorRGB(){
	var intextcolor = document.getElementById("coloreCellaViva");
	var myrgb = new RandomColorRGB();
	console.log("Color is :"+myrgb.randomHexColor());
	intextcolor.value = myrgb.randomHexColor();

}

