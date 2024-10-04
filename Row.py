'''Rows consist of boxes and multiple rows together form a rows list which is an attribute of a node'''
class Row:
    def __init__(self, num, boxes):
        self.num = num  # row num in the board
        self.boxes = boxes  # list of boxes in that row
        self.num_boxes = len(boxes)  # the number of boxes in the row

    ''' makes a copy of itself'''
    def copy(self):
        new_boxes = []
        for box in self.boxes:
            new_boxes.append(box.copy())
        return Row(self.num, new_boxes)
