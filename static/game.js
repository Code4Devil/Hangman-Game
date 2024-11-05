let gameData = {
    word: '',
    display_word: '',
    remaining_tries: 0,
    used_letters: []
};

function startNewGame() {
    fetch('/start_game')
        .then(response => response.json())
        .then(data => {
            gameData = data;
            updateUI();
        });
}

function guessLetter() {
    const letterInput = document.getElementById('letter').value.toLowerCase();
    if (!letterInput || letterInput.length !== 1 || !/^[a-z]$/.test(letterInput)) {
        alert('Please enter a valid letter.');
        return;
    }

    fetch('/guess', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ letter: letterInput })
    })
        .then(response => response.json())
        .then(data => {
            if (data.result === 'win') {
                alert('You win! The word was ' + data.word);
            } else if (data.result === 'lose') {
                alert('You lost! The word was ' + data.word);
            }

            gameData = data;
            updateUI();
        });
}

function updateUI() {
    document.getElementById('word-display').textContent = gameData.display_word.split('').join(' ');
    document.getElementById('tries').textContent = gameData.remaining_tries;
    document.getElementById('used-letters').textContent = gameData.used_letters.join(', ');
}

window.onload = startNewGame;
