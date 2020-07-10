import pygame
import button

pygame.init()
running = True

# Window info
screen_width = 600
screen_height = 200
screen = pygame.display.set_mode((screen_width, screen_height)) # Set display size
pygame.display.set_caption("Dots Puzzle") # Set title
icon = pygame.image.load("circlered.png") # Load icon
pygame.display.set_icon(icon) # Set icon

class Dot():
    def __init__(self, colour, pos, x, y, width, height):
        self.colour = colour
        self.pos = pos
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.clicked = False
        self.highlight = False
        self.dot = button.Button(self.colour, self.x, self.y, self.width, self.height)

    def update_pos(self, new_pos):
        self.pos = new_pos

    def get_direction(self):
        return self.direction

    def click(self, clicked):
        self.clicked = clicked

# Game info
dot_size = 40
dot_pos_x = int(screen_width/8)
dot_pox_y = int(screen_height/2)
spacing = 50
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
font = pygame.font.SysFont("verdana", 32)
text_win = font.render("YOU WIN !", False, RED)

dots = []
buttons = []

# Orders
order_start = [BLACK, BLACK, BLACK, BLACK, WHITE, RED, RED, RED, RED]
order_win = [RED, RED, RED, RED, WHITE, BLACK, BLACK, BLACK, BLACK]
order = [BLACK, BLACK, BLACK, BLACK, WHITE, RED, RED, RED, RED]

# Undo/redo
order_history = [order_start]
step = 0

# Currently clicked button
clicked = None

# Initialize dots
for i in range(len(order_start)):
    dots.append(Dot(order_start[i], i, dot_pos_x + (spacing*i), dot_pox_y, dot_size, dot_size))

# Initialize buttons
buttons.append(button.Button(WHITE, 10, 10, 50, 20, "UNDO"))
buttons.append(button.Button(WHITE, 70, 10, 50, 20, "REDO"))
buttons.append(button.Button(WHITE, 130, 10, 60, 20, "RESTART"))
buttons.append(button.Button(RED, 530, 10, 50, 20, "QUIT"))

def check_win():
    if order == order_win:
        screen.blit(text_win, (246, 21))

def draw_dots():
    for i in range(len(dots)):
        if dots[i].clicked:
            dots[i].dot.draw(screen, GREEN)
        elif dots[i].highlight:
            dots[i].dot.draw(screen, BLUE)
        else:
            dots[i].dot.draw(screen)

def draw_buttons():
    for i in range(len(buttons)):
        buttons[i].draw(screen, BLACK)

def check_clicked():
    for i in range(len(dots)):
        if dots[i].clicked:
            if dots[i].colour == BLACK:
                highlight_dots(i+1, WHITE)
                if dots[i+1].colour == RED:
                    highlight_dots(i+2, WHITE)
            if dots[i].colour == RED:
                highlight_dots(i-1, WHITE)
                if dots[i-1].colour == BLACK:
                    highlight_dots(i-2, WHITE)

def highlight_dots(i, colour):
    try:
        if dots[i].colour == colour:
            dots[i].highlight = True
    except IndexError:
        print("Index out of range")

def swap_dots(first, second):
    colour_1 = dots[first].colour
    colour_2 = dots[second].colour
    assign_colour(first, colour_2)
    assign_colour(second, colour_1)
    step_forward()

def assign_colour(i, colour):
    dots[i].colour = colour
    dots[i].dot.colour = colour
    order[i] = colour

def get_clicked():
    for i in range(len(dots)):
        if dots[i].clicked:
            return i
    return -1

def step_forward():
    global step
    if (len(order_history)-1) > step:
        del order_history[step+1:]
    order_history.append(order.copy())
    step += 1

def undo():
    global step
    if step != 0:
        step -= 1
        for i in range(len(order)):
            assign_colour(i, order_history[step][i])

def redo():
    global step
    if step != (len(order_history)-1):
        step += 1
        for i in range(len(order)):
            assign_colour(i, order_history[step][i])

def restart():
    global order
    global order_history
    global step
    global clicked
    order = order_start.copy()
    order_history = [order_start]
    clicked = None
    step = 0
    for i in range(len(order_start)):
        assign_colour(i, order_start[i])

while running:
    screen.fill((50, 50, 50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in range(len(dots)):
                    if dots[i].dot.is_over(event.pos):
                        if dots[i].highlight:
                            swap_dots(i, get_clicked())
                        else:
                            dots[i].clicked = True
                    dots[i].highlight = False
                for i in range(len(dots)):
                    if not dots[i].dot.is_over(event.pos):
                        dots[i].clicked = False
                for i in range(len(buttons)):
                    if buttons[i].is_over(event.pos):
                        if i == 0:
                            undo()
                        if i == 1:
                            redo()
                        if i == 2:
                            restart()
                        if i == 3:
                            running = False

    check_clicked()
    draw_dots()
    draw_buttons()
    check_win()

    pygame.display.update()