
class Agent:
    def __init__(self, num_plies_ahead):
        self.num_plies_ahead = num_plies_ahead
        self.selected_node = None

    def search(self, environ):
        if self.num_plies_ahead > len(environ.current_node.possible_moves):
            self.num_plies_ahead = len(environ.current_node.possible_moves)
        environ.current_node.children = []
        environ.current_node.is_max = True
        environ.current_node.value = float('-inf')

        self.dfs(environ.current_node, environ)
        # extra linear search - redundant
        environ.current_node = self.selected_node
        print(environ.current_node.get_color("Computer plays..." + environ.current_node.last_move, "AI"))
        return environ.current_node.last_move
        '''for child in environ.current_node.children:
            if child.value == environ.current_node.value:
                print(child.get_color("Computer plays: " + child.last_move, "AI"))
                environ.current_node = child

                return child.last_move'''


    def dfs(self, node, environ):
        max_node_num = -1
        min_node_num = -1
        if node.ply < self.num_plies_ahead + environ.current_node.ply:
            for move in node.possible_moves:
                new_node = node.copy()
                if (node.ply - environ.current_node.ply) % 2 == 0:
                    mover = "AI"
                else:
                    mover = "YOU"
                new_node = environ.update(new_node, int(move[:-1]), move[-1], mover)
                new_node.ply += 1

                node.children.append(new_node)
                self.dfs(new_node, environ)
                if node.stop_exploring:
                    print("dfdfqsafasdfsdf")
                    break

            node.value, self.selected_node, node.children, max_node_num, min_node_num = \
                self.find_max_min(node.children, node.is_max, max_node_num, min_node_num) # not getting triggered enough

        # needs to be beta or alpha for each level?
        # alpha beta cannot be determined for certain until a child is assigned a value
        elif node.ply == self.num_plies_ahead + environ.current_node.ply:
            node.calculate_evaluation()
            '''while node is not None:

                node.value, self.selected_node, node.children, max_node_num, min_node_num = \
                    self.find_max_min(node.children, node.is_max, max_node_num, min_node_num)
                node = node.parent'''

    '''def find_max_min(self, children, is_max):
        min_node = None
        max_node = None
        if is_max:
            max_min_val = float("-inf")
            max_node = None
        else:
            max_min_val = float("inf")
            min_node = None

        for child in children:
            if is_max and child.value > max_min_val:
                if max_node is not None:
                    max_node.stop_exploring = True # not sure will work
                max_node = child
                max_min_val = child.value
            elif not is_max and child.value < max_min_val:
                if min_node is not None:
                    min_node.stop_exploring = True # not sure will work
                min_node = child
                max_min_val = child.value
            else:
                child.stop_exploring = True
        return max_min_value, max_node '''

    def find_max_min(self, children, is_max, max_node_num, min_node_num):

        max_node = None
        if is_max:
            max_min_val = float("-inf")
            max_node = None
        else:
            max_min_val = float("inf")

        for child_num in range(len(children)):
            if is_max and children[child_num].value > max_min_val:
                if max_node_num != -1:
                    children[max_node_num].stop_exploring = True
                max_node_num = child_num
                max_min_val = children[child_num].value
                max_node = children[child_num]
            elif not is_max and children[child_num].value < max_min_val:
                if min_node_num != -1:
                    children[min_node_num].stop_exploring = True
                min_node_num = child_num
                max_min_val = children[child_num].value
            else:
                children[child_num].stop_exploring = True


        return max_min_val, max_node, children, max_node_num, min_node_num
