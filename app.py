from flask import Flask, jsonify, request, render_template
import random

app = Flask(__name__)

# List of possible words for the game
WORDS = ['javascript', 'hangman', 'python', 'flask', 'programming', 'developer', 'frontend', 'backend']
MAX_TRIES = 6

# Initialize game state
game_state = {}

def start_game():
    word = random.choice(WORDS)
    game_state['word'] = word
    game_state['display_word'] = ['_'] * len(word)
    game_state['remaining_tries'] = MAX_TRIES
    game_state['used_letters'] = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['GET'])
def start_new_game():
    start_game()
    return jsonify({
        'word': ''.join(game_state['display_word']),
        'remaining_tries': game_state['remaining_tries'],
        'used_letters': game_state['used_letters']
    })

@app.route('/guess', methods=['POST'])
def guess_letter():
    letter = request.json.get('letter').lower()

    if not letter or len(letter) != 1 or not letter.isalpha():
        return jsonify({'error': 'Invalid letter'}), 400
    
    if letter in game_state['used_letters']:
        return jsonify({'message': 'You already guessed that letter!'}), 400
    
    game_state['used_letters'].append(letter)

    # Check if the guessed letter is in the word
    if letter in game_state['word']:
        for i, char in enumerate(game_state['word']):
            if char == letter:
                game_state['display_word'][i] = letter
        result = 'correct'
    else:
        game_state['remaining_tries'] -= 1
        result = 'incorrect'

    # Check win or lose
    if ''.join(game_state['display_word']) == game_state['word']:
        return jsonify({
            'result': 'win',
            'word': game_state['word'],
            'display_word': ''.join(game_state['display_word']),
            'remaining_tries': game_state['remaining_tries']
        })
    
    if game_state['remaining_tries'] <= 0:
        return jsonify({
            'result': 'lose',
            'word': game_state['word'],
            'display_word': ''.join(game_state['display_word']),
            'remaining_tries': game_state['remaining_tries']
        })
    
    return jsonify({
        'result': result,
        'display_word': ''.join(game_state['display_word']),
        'remaining_tries': game_state['remaining_tries'],
        'used_letters': game_state['used_letters']
    })

if __name__ == '__main__':
    start_game()  # Start a game at the beginning
    app.run(debug=True)
