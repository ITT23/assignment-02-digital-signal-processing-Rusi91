# Created for the application, however, it is obsolete for the simple type of pyglet application.

COLOR_NOT_CHOOSEN = (255,255,255,0)
COLOR_CHOOSEN = (0,255,0,0)

class Rectangle():

    def __init__(self, width, height, position, choosen, x_pos, y_pos):
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = COLOR_NOT_CHOOSEN
        self.position = position
        self.choosen = choosen
        

    def get_color(self):
        if self.choosen == True:
            return COLOR_CHOOSEN
        else:
            return COLOR_NOT_CHOOSEN
    
    def get_x_pos(self):
        return self.x_pos
    
    def get_y_pos(self):
        return self.y_pos

    def set_choosen(self):
        self.choosen = True
        self.color = COLOR_CHOOSEN
    
    def set_not_choosen(self):
        self.choosen = False
        self.color = COLOR_NOT_CHOOSEN

    