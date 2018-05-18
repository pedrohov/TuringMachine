State = function(id, name, x, y) {

	this.id = id;
	this.name = name;
	this.isInitial = false;
	this.isFinal = false;
	this.isCurrent = false;

	this.x = x;
	this.y = y;
	this.radius = 20;
	this.lineColor = '#334A5F';
	this.fillColor = '#49749b';
	this.fillCurrent = '#FF8663';
	this.textColor = '#F0F1F2';

}

State.prototype.constructor = State;

State.prototype.draw = function(context) {

	// Draw circle:
	context.beginPath();
	context.strokeStyle = this.lineColor;
	if(this.isCurrent)
		context.fillStyle = this.fillCurrent;
	else context.fillStyle = this.fillColor;
	context.lineWidth = 2;
	context.arc(this.x, this.y, this.radius, 0, 2 * Math.PI);
	context.fill();
	context.stroke();

	// Draw initial symbol:
	if(this.isInitial) {
		context.beginPath();
		context.moveTo(this.x - this.radius - 35, this.y);
		context.lineTo(this.x - this.radius, this.y);
		context.lineTo(this.x - this.radius - 10, this.y + 10);
		context.moveTo(this.x - this.radius, this.y);
		context.lineTo(this.x - this.radius - 10, this.y - 10);
		context.stroke();
	}

	// Draw final symbol:
	if(this.isFinal) {
		context.beginPath();
		context.arc(this.x, this.y, this.radius * 0.8, 0, 2 * Math.PI);
		context.stroke();
	}

	// Draw name:
	context.font = '14px Arial';
    context.fillStyle = this.textColor;
    context.textAlign = 'center';
    context.textBaseline = 'middle';
    context.fillText(this.name, this.x, this.y);
}