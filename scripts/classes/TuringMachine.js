TuringMachine = function(tape) {
	
	this.states = [];
	this.alphabet = ['_'];
	this.transitions = [];
	this.eInitial = null;
	this.eFinals = [];
	this.tape = tape;

	this.currentState = null;

	//
	this.stateIDseed = 0;
	this.transIDseed = 0;

}

TuringMachine.prototype.constructor = TuringMachine;

TuringMachine.prototype.addState = function(state) {
	this.states.push(state);
}

TuringMachine.prototype.removeState = function() {}

TuringMachine.prototype.addTransition = function(transition) {
	this.transitions.push(transition);
}

TuringMachine.prototype.removeTransition = function(id) {
	for(var i = 0; i < this.transitions.length; i++) {
		if(this.transitions[i].id === id) {
			this.transitions.splice(i, 1);
			return;
		}
	}
}

TuringMachine.prototype.addToAlphabet = function(char) {

	var index = this.alphabet.indexOf(char);
	if(index === -1)
		this.alphabet.push(char);

}

TuringMachine.prototype.step = function() {

	// Initial state:
	if(this.currentState === null) {
		if(this.eInitial === null) {
			alert("Set a initial state.");
			return;
		}

		this.currentState = this.eInitial;
		this.currentState.isCurrent = true;
		this.tape.move('R');
		return;
	}

	// Other states:
	var transition = this.getTransitionFrom(this.currentState.id, this.tape.currentChar());
	
	if(transition === null) {
		alert("No transition from " + this.currentState.name + " reading " + this.tape.currentChar());
	} else {
		this.tape.write(transition.write);
		this.tape.move(transition.move);
		this.currentState.isCurrent = false;
		this.currentState = transition.to;
		this.currentState.isCurrent = true;
	}

}

TuringMachine.prototype.getTransitionFrom = function(stateID, symbol) {

	for(var i = 0; i < this.transitions.length; i++) {
		if((this.transitions[i].from.id === stateID) && (this.transitions[i].read === symbol)) {
			return this.transitions[i];
		}
	}

	return null;
}

TuringMachine.prototype.run = function() {}
TuringMachine.prototype.export = function() {}
TuringMachine.prototype.import = function() {}

TuringMachine.prototype.selectedState = function(x, y) {

	var index = this.states.length - 1;
	while(index >= 0) {
		var state = this.states[index];
		var distance = Math.sqrt((state.x - x) * (state.x - x) + (state.y - y) * (state.y - y));
		if(distance <= state.radius) {
			return state;
		}
		index--;
	}
	return null;

}

TuringMachine.prototype.deleteElementsAt = function(x, y) {

	// Remove states:
	var index = this.states.length - 1;
	while(index >= 0) {
		var state = this.states[index];
		var distance = Math.sqrt((state.x - x) * (state.x - x) + (state.y - y) * (state.y - y));
		if(distance <= state.radius) {

			// If it is a final state, remove it from eFinals:
			var fIndex = this.eFinals.indexOf(state.id);
			this.eFinals.splice(fIndex, 1);

			// If it was the initial state, remove it:
			if(this.eInitial === state.id)
				this.eInitial = null;

			// Remove any transitions connected to it:
			var j = this.transitions.length - 1;
			while(j >= 0) {
				var transition = this.transitions[j];
				if((transition.to.id === state.id) || (transition.from.id === state.id)) {
					this.transitions.splice(index, 1);
				}
				j--;
			}

			// Remove it from the states array:
			this.states.splice(index, 1);
		}

		index--;
	}

	// Remove transitions:
	var j = this.transitions.length - 1;
	while(j >= 0) {
		var transition = this.transitions[j];
		var distance = Math.sqrt((transition.x - x) * (transition.x - x) + (transition.y - y) * (transition.y - y));
		if(distance <= state.radius)
			this.transitions.splice(index, 1);
		j--;
	}

	console.log(this);
}

TuringMachine.prototype.setInitialState = function(x, y) {

	var index = this.states.length - 1;
	while(index >= 0) {
		var state = this.states[index];
		var distance = Math.sqrt((state.x - x) * (state.x - x) + (state.y - y) * (state.y - y));
		if(distance <= state.radius) {
			// Remove previous initial:
			if(this.eInitial !== null) {
				this.eInitial.isInitial = false;
			}

			// Set as initial:
			if(!state.isInitial) {
				state.isInitial = true;
				this.eInitial = state;
			} else {
				state.isInitial = false;
				this.eInitial = null;
			}
		}

		index--;
	}

}

TuringMachine.prototype.setFinalState = function(x, y) {

	var index = this.states.length - 1;
	while(index >= 0) {
		var state = this.states[index];
		var distance = Math.sqrt((state.x - x) * (state.x - x) + (state.y - y) * (state.y - y));
		if(distance <= state.radius) {
			// Set as final:
			if(!state.isFinal) {
				state.isFinal = true;
				this.eFinals.push(state.id); // Add to the finals array.
			} else {
				state.isFinal = false;
				this.eFinals.splice(this.eFinals.indexOf(state.id, 1)); // Remove from the finals array.
			}
		}

		index--;
	}
}