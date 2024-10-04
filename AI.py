import time


'''The agent which using dfs and pruning searches the tree for the optimal moves looking some number of plies ahead
    num_plies_ahead (int) - number of plies to look ahead'''
class AI:
    def __init__(self, num_plies_ahead):
        self.num_plies_ahead = num_plies_ahead
        self.selected_node = None  # best node in the search tree (the node corresponding to the optimal move)

    '''searches for the best move for the agent
        environ (Environment) - the current environment (state of the board, etc)'''
    def search(self, environ):
        print("\nComputer thinking...")
        start = time.time()  # to keep track of how long the search went for
        environ.in_search = True  # boolean used to keep track of if AI is currently searching for move
        # ensures that the agent won't look ahead more plies than it is possible:
        # (if game is done in 3 plies it can't look 4 plies ahead)
        if self.num_plies_ahead > len(environ.current_node.possible_moves):
            self.num_plies_ahead = len(environ.current_node.possible_moves)
        environ.prep_for_dfs()  # resets environment
        self.dfs(environ.current_node, environ)  # begins the depth first search
        environ.current_node = self.selected_node  # sets the current game node to node the agent picked (via its move)
        print("Computer took " + self.calc_move_time(start) + " second(s) thinking.")
        print(environ.current_node.get_color("Computer plays..." + environ.current_node.last_move, "AI"))
        environ.in_search = False # computer has found move (not searching anymore)
        return environ.current_node.last_move  # returns best move

    ''' to calc move time of computer
        start (float) - starting time'''
    def calc_move_time(self, start):
        return str(round(time.time() - start))

    ''' executes depth first search
        node (Node) - node being explored
        environ (Environment) - current environment'''
    def dfs(self, node, environ):
        # if the search depth has not been reached...
        if node.ply < self.num_plies_ahead + environ.current_node.ply:
            # makes children for each possible move
            for move in node.possible_moves:
                new_node = node.copy()
                # the AI and player will alternate moves in these hypothetical nodes
                if (node.ply - environ.current_node.ply) % 2 == 0:
                    mover = "AI"
                else:
                    mover = "YOU"
                # updates node (how the board changed after the hypothetical move)
                new_node = environ.update(new_node, int(move[:-1]), move[-1], mover)
                node.children.append(new_node)
                self.dfs(new_node, environ)  # keep recursing since we're not at proper depth yet
                # if the node has been pruned don't look for more children!
                if node.stop_exploring:
                    break
            # sets node's value to either max or min of its children (based on if node is a max or min node)
            node.value, self.selected_node = self.find_max_min(node)
        # when we reach the proper depth
        elif node.ply == self.num_plies_ahead + environ.current_node.ply:
            node.calculate_evaluation()  # calculate the value of node: ai_pts - player_pts
        # now that the node value has been found update the alpha or beta of parent
        if node.parent is not None:
            node.parent.a_b = self.assign_a_b(node)
            node.parent = self.compare_a_b(node.parent, environ) # determines if we should initiate pruning

    ''' assigns alpha or beta value after one or more childen values have been determined
            node (Node) - the child that recently was assigned a value'''
    def assign_a_b(self, node):
        # if the parent is a max node we need to check if the child exceeds this
        # because the parent's alpha would need to be updated. Vice versa if the parent is a min node (update beta)
        if (node.parent.is_max and node.parent.a_b < node.value) or \
                (not node.parent.is_max and node.parent.a_b > node.value):
            return node.value
        else:
            return node.parent.a_b

    ''' assigns a node to be pruned: if an ancestors alpha exceeds its beta or an ancestors beta is less than its alpha
        node (Node)
        environ (Environment) '''
    def compare_a_b(self, node, environ):
        ancestor = node.parent
        while ancestor is not None and ancestor.ply >= environ.current_node.ply:
            # checks to see if pruning is warranted as described above in function comment
            if (ancestor.is_max and node.a_b <= ancestor.a_b) or (
                    not ancestor.is_max and node.a_b >= ancestor.a_b):
                node.stop_exploring = True  # stop exploring that node (prune)
            # recurses up the tree, after checking parent alpha/ beta vs itself checks great-grandparents alpha/ beta...
            if ancestor.parent is not None:
                ancestor = ancestor.parent.parent
            else:
                ancestor = None
        return node

    ''' finds the min or max of values for a node's children (depending if node is a max or min node)
        node (Node)'''
    def find_max_min(self, node):
        best_node = None
        if node.is_max:
            max_min_val = float("-inf")
        else:
            max_min_val = float("inf")
        for child in node.children:
            if not child.stop_exploring:  # don't look at nodes that have pruned leaves
                # sees if child's value is above max (or below min) so far
                if (node.is_max and child.value > max_min_val) or ((not node.is_max) and child.value < max_min_val):
                    # if so, store its value and itself to return (will be used as best move if node = current_node)
                    max_min_val = child.value
                    best_node = child
        return max_min_val, best_node
