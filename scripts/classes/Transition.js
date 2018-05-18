Transition = function(id, from, to) {

	this.id = id;
	this.from = from;
	this.to = to;
	this.read = null;
	this.write = null;
	this.move = null;

	this.lineColor = '#334A5F';
	this.fillColor = '#49749b';

	this.editRadius = 6;
	this.x = null;
	this.y = null;

}

Transition.prototype.constructor = Transition;

Transition.prototype.draw = function(context) {

	// Draw line:
	context.strokeStyle = this.lineColor;
	var d = (this.from.y - this.to.y) / (this.to.x - this.to.y);
	context.beginPath();
	context.moveTo(this.from.x, this.from.y);
	context.lineTo(this.to.x, this.to.y);
	context.stroke();

	var x = this.to.x;
    if(this.from.x < this.to.x)
    	x = this.from.x
    x += Math.abs(this.to.x - this.from.x) / 2;

    var y = this.to.y 
    if(this.from.y < this.to.y)
    	y = this.from.y;
    y += Math.abs(this.to.y - this.from.y) / 2;

	// Draw info:
	if(this.read !== null) {
		context.font = '20px Arial';
	    context.fillStyle = this.lineColor;
	    context.textAlign = 'center';
	    context.textBaseline = 'middle';

	    context.fillText(this.read + "/" + this.write + ", " + this.move, x, y - 30);
	}

	// Draw edit circle:
	this.x = x;
	this.y = y + 20;
	context.beginPath();
	context.fillStyle = this.fillColor;
	context.arc(this.x, this.y, this.editRadius, 0, 2 * Math.PI);
	context.fill();

}