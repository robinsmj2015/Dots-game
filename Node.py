'''node represents a board state and consists of a list of rows, stores other useful information as described below'''
class Node:
    def __init__(self, ply, rows, parent, last_move):
        self.ply = ply  # ply number of node
        self.rows = rows  # list of rows in board
        self.num_rows = len(rows)  # total number of rows
        self.boxes_per_row = self.rows[0].num_boxes  # number of boxes in a row
        self.num_boxes = self.num_rows * self.boxes_per_row  # number of boxes in board
        self.parent = parent  # parent
        self.ai_pts = 0  # computer points
        self.player_pts = 0  # human points
        self.last_move = last_move  # what the last move was
        self.stop_exploring = False  # if the node's children should not be explored (should be pruned)
        self.children = []  # children
        self.possible_moves = []  # allowed moved from this node
        self.is_max = False  # is the node a max or min node
        self.value = float("inf")  # initial value for node
        self.a_b = float("inf")  # initial alpha or beta value for nod
        self.set_initial_values()  # sets some initial values for node

    ''' sets values for node: including if it should be a max or min node, its possible moves, its alpha or beta value
        and its initial value'''
    def set_initial_values(self):
        if self.parent is not None:
            self.is_max = not self.parent.is_max
            self.possible_moves = self.parent.possible_moves.copy()
        if self.is_max:
            self.value = float("-inf")
            self.a_b = float("-inf")

    ''' copies the node'''
    def copy(self):
        new_rows = []
        for row in self.rows:
            new_rows.append(row.copy())
        node_copy = Node(self.ply, new_rows, self, self.last_move)  # makes a new node
        node_copy.ai_pts = self.ai_pts
        node_copy.player_pts = self.player_pts
        return node_copy

    ''' iterates through the rows and boxes on the board and searches for owned boxes, sums points for ai and player
        returns heuristic value of state'''
    def calculate_evaluation(self):
        for row in self.rows:
            for box in row.boxes:
                if box.scored or box.owner is None:
                    pass
                elif box.owner == "AI":
                    self.ai_pts += box.value  # AI gets points if it owns a box
                    box.scored = True
                else:
                    self.player_pts += box.value  # player gets points if they own a box
                    box.scored = True
        self.value = self.ai_pts - self.player_pts  # returns AI heuristic of state

    ''' prints the board - this is done in a row by row fashion where all the box tops are printed before the middle
        sections before the bottom sections'''
    def display(self):
        for row in self.rows:
            tops = ""
            for box in row.boxes:
                tops += (self.get_color(" --------", box.top))
            print(tops)
            mids = ""
            for box in row.boxes:
                if len(box.num_str) == 2:
                    str_space = " ("
                else:
                    str_space = "("
                if box == row.boxes[0]:
                    mids += self.get_color("| ", box.left)
                mids += self.get_color(box.num_str + str_space + str(box.value) + ")", box.owner) + \
                    self.get_color(" | ", box.right)
            print(mids)
            if row == self.rows[-1]:
                bottoms = ""
                for box in row.boxes:
                    bottoms += self.get_color(" --------", box.bottom)
                print(bottoms)
        # prints the scores of the players
        print(self.get_color("Player score: " + str(self.player_pts), "YOU") +
              self.get_color("\nComputer score: " + str(self.ai_pts), "AI"))

    ''' returns the proper color of the string:
        if the ai moved it is red, if human blue, if the move hasn't been played: grey
        string (str) - string to color
        mover (str) - who played the move'''
    def get_color(self, string, mover):
        if mover == "YOU":
            color = "\033[94m"  # blue u
        elif mover == "AI":
            color = "\033[91m"  # red AI
        else:
            color = "\033[90m"  # grey
        return color + string + "\033[38m"
