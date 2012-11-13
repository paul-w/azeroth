'''
Contains game logic. Interacts directly with database.
'''

def play(inp, database, user_id):

    ''' Executes a turn in the game '''

    append_to_history('', database, user_id)
    history = get_history(database, user_id)
    valid = check_valid_move(inp, database, user_id)
    if valid: 
        action, noun = inp.split(' ')
        if action=='go':
            go(noun, database, user_id)
        elif action=='pickup':
            pickup(noun, database, user_id)
        elif action=='drop':
            drop(noun, database, user_id)
        else:
            raise ValueError, 'invalid action attempted' 
    else: 
        append_to_history('have you gone mad!? such language is forbidden in azeroth!', database, user_id)
    if(game_over(database, user_id)):
        append_to_history('YOU WIN!', database, user_id)
    else:
        append_valid_moves_to_history(database, user_id)

def game_over(database, user_id):

    ''' Determines whether game has ended '''

    if current_location(database, user_id) == 'goal':
        return True
    else:
        return False

def append_valid_moves_to_history(database, user_id):

    ''' Appends moves to history '''

    valid_moves = get_valid_moves(database, user_id)
    a = 'valid moves:'
    for v in valid_moves:
        a = a + '\n' + v
    append_to_history(a, database, user_id) 
    
def new_game(username, password, database):

    ''' Creates a new game. Called upon successful registration '''

    # initialize user
    database.execute(
    'insert into players (location, username, password, history) '
    'values (?, ?, ?, ?)', ('start', username, password, 'welcome to azeroth!'))
    database.commit()
    cur = database.execute(
    'select last_insert_rowid()')
    id, = cur 
    id = id[0]
    database.execute(
        'update players set location=? where id=?', ('start', id,))
    database.commit() 

    # initialize item states
    cur = database.execute('select location, name from items')
    for row in cur:
        loc, name = row
        database.execute('insert into itemstate (player, item, carried, lastloc)'
        'values (?, ?, ?, ?)', (id, name, False, loc))
        database.commit()

    return id

def drop(name, database, user_id):
    
    ''' Causes player to drops item  '''

    loc = current_location(database, user_id) 
    cur = database.execute(
    'update itemstate set carried=?, lastloc=? where player=? and item=?',
    (False, loc, user_id, name))
    database.commit()
    append_to_history('dropped ' + name, database, user_id) 

def pickup(name, database, user_id): 

    ''' Causes player to pick up item  '''

    cur = database.execute(
    'update itemstate set carried=? where player=? and item=?',
    (True, user_id, name))
    database.commit()
    append_to_history('picked up ' + name, database, user_id) 

def go(new_loc, database, user_id):

    ''' Updates a player's location '''
    
    cur = database.execute(
                'update players set location=? where id=?', 
                (new_loc, user_id,))    
    database.commit()
    append_to_history('went to ' + new_loc, database, user_id)

def append_to_history(s, database, user_id):

    ''' Writes string to history '''

    cur = database.execute(
            'select history from players where id=?', (user_id,))
    history, = cur.fetchone() 
    history = str(history)
    updated_history = history + '\n' + s 
    cur = database.execute(
        'update players set history=? where id=?', 
        (updated_history, user_id,))
    database.commit()

def get_history(database, user_id):
    
    ''' Gets history from database'''

    cur = database.execute(
            'select history from players where id=?', (user_id,))
    history, = cur.fetchone() 
    return str(history)

def current_location(database, user_id):

    ''' Returns current location of player '''

    cur = database.execute(
            'select location from players where id=?', (user_id,))
    loc, = cur
    loc = str(loc[0])
    return str(loc)

def get_valid_moves(database, user_id):

    ''' Returns which moves are valid '''

    # items
    valid_moves = [] 
   
    # picking up items
    current_loc = current_location(database, user_id)
    cur = database.execute(
            'select name from itemstate, items ' 
            'where lastloc=? and carried=? and player=? and items.name=itemstate.item', 
    (current_loc, False, user_id))
    for row in cur:
        item, = row
        s = 'pickup ' + item
        if s not in valid_moves:
            valid_moves.append(s)
    
    # dropping items
    cur = database.execute(
    'select item from itemstate '
    'where carried=? and player=?',
    (True, user_id))
    for row in cur:
        item, = row
        s = 'drop ' + item
        if s not in valid_moves:
            valid_moves.append(s)

    # going places 
    neighboring_locs = [] 
    cur = database.execute(
          'select right from paths where left=?', (current_loc,))
    for row in cur:
        loc, = row
        neighboring_locs.append(loc)
    cur = database.execute(
          'select left from paths where right=?', (current_loc,))
    for row in cur:
        loc, = row
        neighboring_locs.append(loc)
    for neighbor in neighboring_locs:
        valid_moves.append(str('go ' + neighbor))

    return valid_moves 

def check_valid_move(inp, database, user_id):

    ''' Checks whether a move valid '''

    valid_moves = get_valid_moves(database, user_id)
    if inp in valid_moves:
        return True
    else:
        return False
