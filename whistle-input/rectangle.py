from pyglet import app, image, clock

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

    def draw_rectangle(self):
        rectangle = image.create(self.width, self.height, self.color)
        rectangle.blit(self.x_pos, self.y_pos)

    def set_choosen(self):
        self.choosen = True
        self.color = COLOR_CHOOSEN
    
    def set_not_choosen(self):
        self.choosen = False
        self.color = COLOR_NOT_CHOOSEN

    