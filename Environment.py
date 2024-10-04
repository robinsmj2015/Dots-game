from Box import Box
from Row import Row
from Node import Node
import random

''' keeps track of the current state of the board via the current node
    dimensions (int) - dimensions of the board'''
class Environment:
    def __init__(self, dimensions):
        self.current_node = None   # the current game state
        self.equivalent_moves = {}  # dictionary mapping moves to their equivalent moves (or None)
        self.make_root(dimensions)  # generates the root node
        self.gen_possible_moves(self.current_node)  # makes a list of all possible moves
        self.current_node.display()  # prints the first node (game state)
        self.in_search = False  # if the agent is currently searching for a move or not

    ''' when the game starts makes a list of all possible moves and removes redundant ones 
        (ie 0R = 1L, a box's right side is his neighbors left side)'''
    def gen_possible_moves(self, node):
        positions = ["L", "R", "T", "B"]
        # for every box and every position...
        for box_num in range(node.num_boxes):
            for pos in positions:
                move = str(box_num) + pos
                # returns equivalent move and discards them from possible moves list if present
                equiv_move = self.get_redundant_move(pos, box_num, node.boxes_per_row, box_num // node.boxes_per_row, len(node.rows))
                self.equivalent_moves[move] = equiv_move
                if equiv_move is not None:
                    self.equivalent_moves[equiv_move] = move  # putting moves and equivalent moves in dict
                node.possible_moves.append(move)
                if equiv_move in node.possible_moves:
                    node.possible_moves.remove(equiv_move)

    ''' resets the current node before the agent starts searching'''
    def prep_for_dfs(self):
        self.current_node.children = []
        self.current_node.is_max = True
        self.current_node.value = float('-inf')
        self.current_node.a_b = float('-inf')

    ''' gets the user's move and checks if it is valid, return the move
        possible moves (str[]) - list of allowed moves in this node'''
    def get_human_move(self, possible_moves):
        print(">>> YOUR TURN >>>")
        is_inpt_valid = False
        while not is_inpt_valid:
            inpt = input("Enter a box number followed by T/B/L/R (for top, bottom, left, right), ie 01T:\n").\
                replace(" ", "").replace(",", "").upper()
            if inpt != "":
                pos = inpt[-1]
                box_num = inpt[:-1]
                if box_num.isnumeric() and int(box_num) < self.current_node.num_boxes:
                    move = str(int(box_num)) + pos
                    # sees if users move or an equivalent move is allowed
                    if move in possible_moves or self.equivalent_moves[move] in possible_moves:
                        is_inpt_valid = True
        return int(box_num), pos

    ''' returns an equivalent move
        pos (str) - which side of the box was drawn in
        box_num (int) - which box was modified in the row
        boxes_per_row (int)
        row_num(int)
        max_rows (int) -how many rows there are'''
    def get_redundant_move(self, pos, box_num, boxes_per_row, row_num, max_rows):
        # looks for equivalent sides and returns none if not any found
        # (ie if a top side is drawn in the top row, there will be no equivalent move)
        if pos == "T":  # top side
            if row_num == 0:
                return None
            new_box_num = box_num - boxes_per_row
            new_pos = "B"
        elif pos == "B":  # bottom side
            if row_num == max_rows - 1:
                return None
            new_box_num = box_num + boxes_per_row
            new_pos = "T"
        elif pos == "L":  # left side
            if box_num % boxes_per_row == 0:
                return None
            new_box_num = box_num - 1
            new_pos = "R"
        else:  # right side
            if (box_num % boxes_per_row) + 1 == boxes_per_row:
                return None
            new_box_num = box_num + 1
            new_pos = "L"
        return str(new_box_num) + new_pos  # returns new move (equivalent one)

    ''' generates the root node
        dimensions (int) - the dimensions of the board'''
    def make_root(self, dimensions):
        rows = []
        num = 0
        row_num = 0
        for r in range(dimensions):  # rows
            row = []
            for c in range(dimensions):  # columns
                row.append(Box(num, row_num, random.randint(1, 5)))  # makes a new box and appends it to a row
                num += 1
            rows.append(Row(row_num, row))  # makes a list of rows
            row_num += 1
        self.current_node = Node(0, rows, None, None)  # makes the root node

    ''' updates equivalent moves for the node
        node (Node) - the node to update
        box (Box) - the box to update
        final_box_num (int) - the box number in the node
        pos (str) - which side to update
        mover (str) - who made the last move'''
    def update_equivalent_side(self, node, box, final_box_num, pos, mover):
        move = str(final_box_num) + pos
        equiv_move = self.equivalent_moves[move]
        # if there aren't any equivalent nodes just return
        if equiv_move is None:
            return None, node
        # updates the equivalent sides as appropriate
        if pos == "T":  # top
            row_above = node.rows[box.row - 1]
            new_box = row_above.boxes[box.num % row_above.num_boxes]
            new_box.bottom = mover
        elif pos == "B":  # bottom
            row_below = node.rows[box.row + 1]
            new_box = row_below.boxes[box.num % row_below.num_boxes]
            new_box.top = mover
        elif pos == "L":  # left
            new_box = node.rows[box.row].boxes[box.num % node.boxes_per_row - 1]
            new_box.right = mover
        else:  # right
            new_box = node.rows[box.row].boxes[box.num % node.boxes_per_row + 1]
            new_box.left = mover
        new_box = self.set_box_owner(new_box, mover)  # sets box owner
        return equiv_move, node

    ''' updates the board position
        node (Node) - the node to update (since a move or hypothetical move was made)
        final_box_num (int) - the box num that the move was played in
        pos (str) - which side of the box was last drawn
        mover (str) - who made the last move'''
    def update(self, node, final_box_num, pos, mover):
        row_num = int(final_box_num // node.boxes_per_row)
        box_num = int(final_box_num % node.boxes_per_row)
        box = node.rows[row_num].boxes[box_num]  # the box to be modified
        # updates equivalent side if the left box's right side was drawn then the right box's left side was drawn... etc
        equiv_move, node = self.update_equivalent_side(node, box, final_box_num, pos, mover)
        # assigns the box side to who made the move
        if pos == "T":
            box.top = mover
        elif pos == "B":
            box.bottom = mover
        elif pos == "R":
            box.right = mover
        else:
            box.left = mover
        box = self.set_box_owner(box, mover)  # sets box's owner
        node.calculate_evaluation()  # calculates the heuristic of the node (ai_pts - player_pts)
        node.last_move = str(box.num) + pos
        # removes the move from possible moves ... varies if depth first search is used or if human made move
        if self.in_search:
            node.possible_moves.remove(node.last_move)
        else:
            if equiv_move in node.possible_moves:
                node.possible_moves.remove(equiv_move)
            if node.last_move in node.possible_moves:
                node.possible_moves.remove(node.last_move)
        node.ply += 1
        return node

    ''' determines the owner of box by looking at who drew the last line
        box (Box) - the box in question
        mover (str) - who drew the last line of the box'''
    def set_box_owner(self, box, mover):
        box.occupied_sides = 0
        # iterates through all sides
        for box_side in [box.left, box.right, box.top, box.bottom]:
            if box_side is not None:
                box.occupied_sides += 1
        if box.occupied_sides == 4:
            box.owner = mover # sets box owner (will be used for scoring later)
        return box

    ''' displays game results'''
    def end_game(self):
        if self.current_node.ai_pts > self.current_node.player_pts:
            print("YOU LOST")
        elif self.current_node.ai_pts < self.current_node.player_pts:
            print("YOU WON")
        else:
            print("TIE GAME")
