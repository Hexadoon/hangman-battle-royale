'''
Main file for HBR Flask app
'''

from flask import (Flask, render_template, session, request, redirect, url_for,
                   flash)

from util import db

app = Flask(__name__)
app.secret_key = "beansbeansbeansbeans"


@app.route('/', methods=["GET", "POST"])
def index():
    '''
    Display index page, for logging in or signing up
    Redirects to /lobby if logged in
    '''
    if 'username' in session:
        return redirect(url_for('lobby'))
    return render_template('index.html')


@app.route('/login', methods=["POST"])
def login():
    '''
    Attempt to login
    Flash if failure
    Redirects to index
    '''
    username, password = request.form['username'], request.form['password']
    if db.login_attempt(username, password):
        session['username'] = username
    else:
        flash('Username or password incorrect!', 'danger')
    return redirect(url_for("index"))


@app.route('/signup', methods=["POST"])
def signup():
    '''
    Attempt to sign up
    Flash if failure
    Redirect to index
    '''
    username, password = request.form['username'], request.form['password']
    if db.signup_attempt(username, password):
        flash('Success! Please log in', 'success')
    else:
        flash('Username already exists!', 'danger')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('index'))


@app.route('/lobby')
def lobby():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('lobby.html')


@app.route('/join_game')
def join_game():
    if 'username' not in session:
        return redirect(url_for('index'))
    username = session['username']
    game_id = db.join_game(username)
    return redirect(url_for("game", game_id=game_id))


@app.route('/game/<game_id>')
def game(game_id):
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('game.html')


@app.route('/get_move/<game_id>', methods=["POST"])
def get_move(game_id):
    if 'username' not in session:
        return 'go away'

    last_move = request.form['last_move']

    move = db.get_move(game_id, ignore=last_move)

    if move is None:
        return 'wait'

    return move


@app.route('/send_move/<game_id>', methods=["POST"])
def send_move(game_id):
    move = request.form['move']

    db.add_move(game_id, move, accesses=7)

    return 'Done'


if __name__ == '__main__':
    app.debug = True
    app.run()
