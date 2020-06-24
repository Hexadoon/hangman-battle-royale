class Player {
	constructor(name, word) {
		this.name = name;
		this.word = word;
		this.guessed = new Set();
		this.lives = 0;
		this.dead = false;
	}
}

var State = {
	playerInfo: []	
}

// playerData should include the name and word of all players, separated by spaces
// eg: Joan Beans Sammy Oldies Jake Lozenge 
function gameStart(playerData) {
	playerData = playerData.split(' ');

	for(let i = 0; i < playerData.length; i += 2) {
		State.playerInfo[i/2] = new Player(playerData[i], playerData[i+1].toLowerCase());
	}
}	

// checks if the player is dead, sets the field accordingly
// NOTE: players cannot come back from the dead, so why waste time checking if they are?
function checkDeath(player) {
	if(player.dead) return;

	if(player.lives >= 6) {
		player.dead = true;
		return;
	}

	for(let i = 0; i < player.word.length; ++i) {
		if(!player.guessed.has(player.word[i])) return;
	}
	player.dead = true;
}

// guessMessage is of the form <offense player number><letter><defense player number>
// eg if player 1 guesses the letter 'n' on player 4, the message is '1n4'
function updateState(guessMessage) {
	if(guessMessage.length != 3) {
		return 'invalid message';
	}
	
	offense = State.playerInfo[guessMessage[0]-1];
	letter = guessMessage[1];
	defense = State.playerInfo[guessMessage[2]-1];
	
	defense.guessed.add(letter);
	if(!defense.word.includes(letter)) {
		offense.lives += 1;
	}
	checkDeath(defense);
	checkDeath(offense);
}

function getPlayerGuess() {

}

function printState() {
	for(let i = 0; i < State.playerInfo.length; ++i) {
		let player = State.playerInfo[i];
		console.log(player);
	}
	console.log();
}

/*
function test() {
	gameStart("Joan Beans Sammy Oldies Jake Lozenge");
	printState();

	// test incorrect guess
	updateState('1c3');
	printState();

	// test correct guess
	updateState('1z3');
	printState();

	// test death by guess
	updateState('1l3');
	updateState('1o3');
	updateState('1e3');
	updateState('1n3');
	updateState('1g3');
	printState();

	// test death by parts
	updateState('1v2');
	updateState('1w2');
	updateState('1x2');
	updateState('1y2');
	updateState('1z2');
	printState();
}
*/

//test();
