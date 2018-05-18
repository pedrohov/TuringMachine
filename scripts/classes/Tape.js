Tape = function(canvas, context) {

	this.input = "";
	this.position = -1;

	this.context = context;
	this.width = canvas.width;
	this.height = 60;
	this.fillColor = '#334A5F';
	this.textColor = '#F0F1F2';
	this.textColorCurrent = '#FF8663';

}

Tape.prototype.constructor = Tape;

Tape.prototype.draw = function () {

	// 
	this.context.fillStyle = this.fillColor;
	this.context.fillRect(0, 0, this.width, this.height);

	// Draw input:
	this.context.font = '25px Arial';
    this.context.fillStyle = this.textColor;
    this.context.textAlign = 'center';
    this.context.textBaseline = 'middle';
	var n = this.input.length;
	var xi = (this.width / 2) - ((n / 2) * 30);
	for(var i = 0; i < n; i++) {

		if(i === this.position)
			this.context.fillStyle = this.textColorCurrent;
		else this.context.fillStyle = this.textColor;

		this.context.fillText(this.input[i], xi, this.height / 2)
		xi += 30;
	}

    // Draw cursor at the current position:
    var x = (this.width / 2) - ((n / 2) * 30) + (30 * this.position);
    var y = this.height;
    var size = 10;

    context.beginPath();
	context.moveTo(x - size, y);
	context.lineTo(x, 50);
	context.lineTo(x + size, y);
	context.lineTo(x - size, y);
	context.fill();

}

Tape.prototype.loadString = function(input) {

	this.input = input;
	this.draw();

}

Tape.prototype.currentChar = function() {
	return this.input[this.position];
}

Tape.prototype.write = function(symbol) {
	this.input[this.position] = symbol;
}

Tape.prototype.move = function(direction) {
	if(direction === 'L')
		this.position--;
	else if(direction === 'R')
		this.position++;
}