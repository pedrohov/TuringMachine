// Variables to draw on canvas:
var canvas = document.getElementById("canvas");
var context = canvas.getContext("2d");

var selected = "";
var tape = new Tape(canvas, context);
var tmachine = new TuringMachine(tape);

// 
var newTransition = null;
var iniState = {x: null, y: null};
var endState = {x: null, y: null};

// Wait for the page to load:
$(document).ready(function() {

	redrawMachine();

	// Mouse input:
	canvas.addEventListener("click", function(event) {
		var canvasRect = canvas.getBoundingClientRect();
		var x = event.clientX - canvasRect.left;
		var y = event.clientY - canvasRect.top;

		executeClick(x, y);
	});

});

function executeClick(x, y) {

	if(selected === "newState") {
		var name = prompt("State name: ");
		if(name === null || name === "")
			return;

		var state = new State(tmachine.stateIDseed, name, x, y);
		state.draw(context);
		tmachine.stateIDseed++;
		tmachine.addState(state);
		console.log(tmachine);
	} else if (selected === "newTransition") {
		var state = tmachine.selectedState(x, y);
		if(state !== null) {
			if(iniState.x === null) {
				iniState.x = x;
				iniState.y = y;
			} else {
				endState.x = x;
				endState.y = y;

				var transition = new Transition(tmachine.transIDseed,
					tmachine.selectedState(iniState.x, iniState.y),
					tmachine.selectedState(endState.x, endState.y));

				tmachine.transIDseed++;
				transition.draw(context);
				tmachine.addTransition(transition);
				console.log(transition);
				newTransition = transition;

				// Reset state coordinates:
				iniState = {x: null, y: null};
				endState = {x: null, y: null};

				// Show new transition meny:
				$('.newTransition').css('display', 'table');
			}
		} else {
			// Reset state coordinates:
			iniState = {x: null, y: null};
			endState = {x: null, y: null};
		}
	} else if (selected === "delete") {
		tmachine.deleteElementsAt(x, y);
	} else if(selected === "setInitial") {
		tmachine.setInitialState(x, y);
	} else if (selected === "setFinal") {
		tmachine.setFinalState(x, y);
	}

	// Draw states and transitions again:
	redrawMachine();
}

function redrawMachine() {
	context.clearRect(0, 0, canvas.width, canvas.height);
	tmachine.transitions.forEach(function(transition) {
		transition.draw(context);
	});
	tmachine.states.forEach(function(state) {
		state.draw(context);
	});
	tmachine.tape.draw();

	$('#alphabet').html("<b>ALPHABET</b>: { " + tmachine.alphabet + " }");
}

function menuSelect(element, option) {
	// Change current option:
	selected = option;
	
	// Deselect previous option:
	$("li").removeClass("selected");

	// Show current selected option:
	$(element).addClass("selected");

	if(selected === "step") {
		tmachine.step();
		redrawMachine();
	}
}

function loadString() {
	var inputString = document.getElementById("strInput").value;

	if(inputString === "" || inputString === null) {
		$('.helpLog').html("Invalid string.");
		$('.helpLog').css("color", "red");
	} else {
		$('.helpLog').html("String loaded.");
		$('.helpLog').css("color", "#2195D6");
		tape.loadString(inputString);
	}
}

function cancelNewTransition() {

	tmachine.removeTransition(newTransition.id);
	redrawMachine();
	$('.newTransition').css('display', 'none');

}

function finishTransition() {
	var read = document.getElementById("transRead").value;
	var write = document.getElementById("transWrite").value;
	var move = document.getElementsByName("direction")[0].checked; /* Left radio */

	if(read === "")
		read = '_';
	if(write === "")
		write = '_';

	// Transition parameters:
	newTransition.read = read;
	newTransition.write = write;
	if(move)
		newTransition.move = 'L';
	else
		newTransition.move = 'R';


	// Add characters to the machine's alphabet:
	tmachine.addToAlphabet(read);
	tmachine.addToAlphabet(write);

	redrawMachine();
	$('.newTransition').css('display', 'none');
}