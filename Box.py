''' Box consists of top left right bottom sides, a list of boxes is used to make a row'''
class Box:
    def __init__(self, num, row, value):
        self.num = num  # number of the box in the row
        self.row = row  # row that the box is in
        self.value = value  # point value of the box
        self.left = None  # who drew the left side of the box
        self.right = None  # who drew the right side of the box
        self.top = None  # who drew the top of the box
        self.bottom = None  # who drew the bottom of the box
        self.owner = None  # who completed the box
        self.occupied_sides = 0  # how many sides of the box are 'drawn in'
        self.scored = False  # has the box been scored yet
        self.num_str = ""  # the num of the box in string form (used in displaying it)
        self.get_str_num()  # makes the string form of the box num (used in displaying the box)

    ''' converts the box number into string, padding a left 0 if the num is less than 10'''
    def get_str_num(self):
        if len(str(self.num)) == 1:
            self.num_str = "0" + str(self.num)
        else:
            self.num_str = str(self.num)

    '''makes a copy of itself'''
    def copy(self):
        new_box = Box(self.num, self.row, self.value)
        new_box.left = self.left
        new_box.right = self.right
        new_box.top = self.top
        new_box.bottom = self.bottom
        new_box.owner = self.owner
        new_box.occupied_sides = self.occupied_sides
        new_box.scored = self.scored
        new_box.num_str = self.num_str
        return new_box
