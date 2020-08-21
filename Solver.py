import time
from Pyraminx import inverse, apply_move, apply_moves, moves
from SolvedStates import solved, solved_V, solved_layer, solved_top, solved_face
from SolvedStates import solved_pseudo_V, solved_1flip_top, solved_keyhole_top

phase_1_states = {}

#-------------------------------------------------------------------------------

'''Return True if state matches a solved_state. Otherwise return False.
solved_state can be a string or a list of strings. Each string may use * as a
wildcard.'''
def is_solved(state, solved_state=solved):
    if isinstance(solved_state, str):
        if solved_state.find("*") == -1:
            return state == solved_state
        else:
            for i in range(len(state)):
                if solved_state[i] != "*" and state[i] != solved_state[i]:
                    return False
            return True
    elif isinstance(solved_state, list):
        for solved_state_i in solved_state:
            if is_solved(state, solved_state_i):
                return True
        return False
    return False

#-------------------------------------------------------------------------------

'''Return all optimal solutions to the given state which bring it to a
desired solved_state.'''
def solve_state(state, solved_state=solved):
    start_time = time.time()

    solutions = []

    # If state is already solved, return
    if is_solved(state, solved_state):
        print("Solution found at depth 0:")
        solutions.append("Already solved")
        return solutions

    # If solved_state is one state
    if isinstance(solved_state, str) and solved_state.find("*") == -1:
        # Populate phase_1_states
        setup(solved_state)

        # Use phase_1_states to search up to depth 4
        potential_solution = phase_1_states.get(state)
        if potential_solution is None:
            print("Depths 1-4 searched in " + str(time.time() - start_time))
        else:
            solutions.append(inverse(potential_solution))
        if len(solutions) > 0:
            print("Solution(s) found at depth " + str(len(potential_solution.split(" "))) + ":")
            return solutions

        # If no solutions found yet, search deeper
        small_list = {} # States in previous depths
        big_list = {} # States in previous depths and current depth

        # Check 1 move away from state
        for move in moves:
            new_state = apply_move(state, move)
            potential_solution = phase_1_states.get(new_state)
            if potential_solution is not None:
                solutions.append(move + " " + inverse(potential_solution))
            small_list[new_state] = move
        if len(solutions) > 0:
            print("Solution(s) found at depth 5:")
            return solutions
        print("Depth 5 searched in " + str(time.time() - start_time))

        # Check all further depths
        depth = 6
        while depth < 12:
            for item in small_list:
                for move in moves:
                    moves_so_far = small_list[item]
                    if moves_so_far.split(" ")[-1][0] != move[0]:
                        new_state = apply_move(item, move)
                        potential_solution = phase_1_states.get(new_state)
                        if potential_solution is not None:
                            solutions.append(moves_so_far + " " + move + " " + inverse(potential_solution))
                        if small_list.get(new_state) is None:
                            big_list[new_state] = moves_so_far + " " + move
            if len(solutions) > 0:
                print("Solution(s) found at depth " + str(depth) + ":")
                return solutions
            small_list = big_list.copy()
            print("Depth " + str(depth) + " searched in " + str(time.time() - start_time))
            depth += 1

    # If solved state is more than one state
    else:
        # Search depth 1
        small_list = {}
        big_list = {}
        for move in moves:
            new_state = apply_move(state, move)
            if is_solved(new_state, solved_state):
                solutions.append(move)
            small_list[move] = new_state
        if len(solutions) > 0:
            print("Solution(s) found at depth 1:")
            return solutions
        print("Depth 1 searched in " + str(time.time() - start_time))

        # Search all further depths
        depth = 2
        while depth < 12:
            for item in small_list:
                for move in moves:
                    if item.split(" ")[-1][0] != move[0]:
                        new_state = apply_move(small_list[item], move)
                        if is_solved(new_state, solved_state):
                            solutions.append(item + " " + move)
                        big_list[item + " " + move] = new_state
            if len(solutions) > 0:
                print("Solution(s) found at depth " + str(depth) + ":")
                return solutions
            small_list = big_list.copy()
            print("Depth " + str(depth) + " searched in " + str(time.time() - start_time))
            depth += 1

    return ["No solution found - the given solved state cannot be reached from the given state."]

#-------------------------------------------------------------------------------

'''Return all optimal solutions to the given scramble which bring it to a
desired solved_state.'''
def solve_scramble(scramble, solved_state=solved):
    return solve_state(apply_moves(solved, scramble), solved_state)

#-------------------------------------------------------------------------------

'''Store the first 4 moves.'''
def setup(solved_state):
    # print("Setting up...")
    # start_time = time.time()

    small_list = {}
    big_list = {}

    phase_1_states.clear()
    
    for move in moves:
        new_state = apply_move(solved_state, move)
        small_list[new_state] = move
        phase_1_states[new_state] = move

    depth = 2
    while depth < 5:
        for state in small_list:
            for move in moves:
                moves_so_far = small_list[state]
                if moves_so_far.split(" ")[-1][0] != move[0]:
                    new_state = apply_move(state, move)
                    big_list[new_state] = moves_so_far + " " + move
                    # print(str(depth) + ": " + moves_so_far + " " + move)
                    if phase_1_states.get(new_state) is not None:
                        pass
                    else:
                        phase_1_states[new_state] = moves_so_far + " " + move
        small_list = big_list.copy()
        depth += 1
    # print("Set up in " + str(time.time() - start_time))

#-------------------------------------------------------------------------------

'''Print all optimal solutions to the given scramble which bring it to a
desired solved_state.'''
def solve(scramble, solved_state=solved):
    response = solve_scramble(scramble, solved_state)
    for solution in response:
        print(solution)
