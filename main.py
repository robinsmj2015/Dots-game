from AI import AI
from Environment import Environment

''' ====================================================== USER INPUT FUNCTIONS =============================================================='''
''' Queries the user for the dimensions of the board'''
def get_dimensions():
    inpt = ""
    while not inpt.isnumeric() or int(inpt) <= 0:
        inpt = input("Enter board dimensions:\n").replace(" ", "").lower()
    return int(inpt)

'''Queries the user for the number of plies ahead that the agent should look'''
def get_plies_ahead():
    inpt = ""
    while inpt == "" or not inpt.isnumeric() or int(inpt) <= 0:
        inpt = input("How many plies should the AI look ahead? (Enter an integer above zero):\n").replace(" ", "")
    return int(inpt)

''' ============================================================ MAIN ===================================================='''
ai = AI(get_plies_ahead())  # makes the agent that will search the proper number of plies ahead
environ = Environment(get_dimensions())  # builds the environment and board with the specified dimensions by user
# loops until game ends
while len(environ.current_node.possible_moves) > 0:
    box_num, pos = environ.get_human_move(environ.current_node.possible_moves) # gets the player's move
    # updates the current_node and game state
    environ.current_node = environ.update(environ.current_node, box_num, pos, "YOU")
    environ.current_node.display()  # displays the board
    ai_move = ai.search(environ)  # AI searches for best move and returns it
    # updates the current_node and game state
    environ.current_node = environ.update(environ.current_node, int(ai_move[:-1]), ai_move[-1], "AI")
    environ.current_node.display()  # displays the board
environ.end_game()  # displays who won
