moves = { "U": [[4, 5, 0, 1, 2, 3, 6, 7, 8, 9, 10, 11], [1, 0, 0, 0]],
         "U'": [[2, 3, 4, 5, 0, 1, 6, 7, 8, 9, 10, 11], [2, 0, 0, 0]],
          "R": [[0, 1, 2, 3, 7, 6, 9, 8, 4, 5, 10, 11], [0, 1, 0, 0]],
         "R'": [[0, 1, 2, 3, 8, 9, 5, 4, 7, 6, 10, 11], [0, 2, 0, 0]],
          "L": [[11, 10, 2, 3, 4, 5, 0, 1, 8, 9, 7, 6], [0, 0, 1, 0]],
         "L'": [[6, 7, 2, 3, 4, 5, 11, 10, 8, 9, 1, 0], [0, 0, 2, 0]],
          "B": [[0, 1, 9, 8, 4, 5, 6, 7, 11, 10, 2, 3], [0, 0, 0, 1]],
         "B'": [[0, 1, 10, 11, 4, 5, 6, 7, 3, 2, 9, 8], [0, 0, 0, 2]] }

#-------------------------------------------------------------------------------

'''Return the inverse of a sequence of moves.'''
def inverse(moves):
    temp = moves.split(" ")
    temp.reverse()
    for i in range(len(temp)):
        if len(temp[i]) == 2:
            temp[i] = temp[i][0]
        else:
            temp[i] += "'"
    return " ".join(temp)

#-------------------------------------------------------------------------------

'''Apply a valid move to the given state.'''
def apply_move(state, move):
    change = moves[move]
    cycle = change[0]
    centers = change[1]
    
    new_state = ""
    for sticker in cycle:
        new_state += state[sticker]
    for i in range(len(centers)):
        center = centers[i]
        new_state += str((int(state[12 + i]) + center) % 3)

    return new_state

#-------------------------------------------------------------------------------

'''Apply a valid sequence of moves to the given state.'''
def apply_moves(state, moves):
    moves = moves.split(" ")
    new_state = state
    for move in moves:
        new_state = apply_move(new_state, move)
    return new_state
