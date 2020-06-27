'''
File for comunicating with the database
'''

import uuid
import sqlite3

# DB_FILE = '/var/www/HBR/HBR/data/hbr.db'
DB_FILE = 'data/hbr.db'


def create_db():
    '''
    Creates the tables in the DB file
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, \
              password TEXT)')

    c.execute('CREATE TABLE IF NOT EXISTS moves(game_id TEXT PRIMARY KEY, \
               move TEXT, accesses INT)')

    c.execute('CREATE TABLE IF NOT EXISTS games(game_id TEXT PRIMARY KEY, \
               players TEXT, player_count INT)')

    c.execute('CREATE TABLE IF NOT EXISTS words(word TEXT, category TEXT)')

    db.commit()
    db.close()

    return True


def login_attempt(username, password):
    '''
    Attempt to login
    Returns True if user/pass combo is correct
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    p = c.fetchone()

    if p is None:
        return False

    return password == p[0]


def user_exists(username):
    '''
    True if username is in DB
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT 1 FROM users WHERE username = ?', (username,))
    check = c.fetchone()

    return check is not None


def signup_attempt(username, password):
    '''
    Attempt to sign up
    Return True if username does not exist and has been added
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if user_exists(username):
        return False

    c.execute('INSERT INTO users VALUES(?, ?)', (username, password))

    db.commit()
    db.close()

    return True


def create_game(host):
    '''
    Creates a game given a inital host username
    Returns game_id
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    game_id = str(uuid.uuid4())
    c.execute('INSERT INTO games VALUES(?, ?, ?)', (game_id, host, 1))

    db.commit()
    db.close()

    return game_id


def join_game(player):
    '''
    Adds player to an existing game
    If no game exists, creates a game with player as host
    Returns game_id
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # Get all awaiting games
    c.execute('SELECT * FROM games')
    games = c.fetchall()

    # If no awaiting games, create a game
    if len(games) == 0:
        game_id = create_game(player)
    # Otherwise, join the awaiting game. Will only ever be one
    else:
        game_id = games[0][0]
        players = games[0][1] + ";" + player
        player_count = games[0][2] + 1
        c.execute('UPDATE games SET players = ? WHERE game_id = ?',
                  (players, game_id))
        c.execute('UPDATE games SET player_count = ? WHERE game_id = ?',
                  (player_count, game_id))
        db.commit()
        db.close()

    return game_id


# TODO: document
def add_word(word, category):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('INSERT INTO words VALUES(?, ?)', (word, category))

    db.commit()
    db.close()


# TODO: document
def check_word(word, category):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT category FROM words WHERE word = ?', (word,))
    categories = list(map(lambda x: x[0], c.fetchall()))

    return category in categories


# TODO: document
def get_words(category):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT word FROM words WHERE category = ?', (category,))
    words = list(map(lambda x: x[0], c.fetchall()))

    print(words)
    return words


# TODO: document
def add_move(game_id, move, accesses):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # TODO: Maybe check for game_id existance first

    c.execute('INSERT INTO moves VALUES(?, ?, ?)', (game_id, move, accesses))

    db.commit()
    db.close()

    return True


# TODO: document
def get_move(game_id, ignore=""):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT move, accesses FROM moves WHERE game_id = ?',
              (game_id,))

    pair = c.fetchone()

    if len(pair) == 0:
        return None

    move, accesses = pair

    if move == ignore:
        return "wait"

    if accesses == 1:
        c.execute('DELETE FROM moves WHERE game_id = ?', (game_id,))
    else:
        c.execute('UPDATE moves SET accesses = ? WHERE game_id = ?',
                  (accesses - 1, game_id))

    db.commit()
    db.close()

    return move


def test():
    # create_game('Joan')
    # join_game('Kevin')
    #
    # add_word('Cheetos', 'Food')
    # add_word('Cheetos', 'Chips')
    # add_word('Cheetah', 'Animals')
    # add_word('Lion', 'Animals')
    #
    # check_word('Cheetos', 'Food')
    # check_word('Cheetos', 'Chips')
    # check_word('Cheetos', 'Bees')
    # check_word('Lion', 'Animals')
    #
    # get_words('Animals')
    # get_words('Food')

    signup_attempt('Joan', 'password')
    signup_attempt('Joan', 'pee')
    user_exists('Joan')
    user_exists('Kevin')


if __name__ == '__main__':
    create_db()
    test()
