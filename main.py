"""
TODO:
- make it so that the cubic bezier is a class that inherits from Line
- also re-add ability to do quadratic bezier
- fix carrot point thin
- rename carrot to control point
- make theta follow control point 
""" 


import pygame
import math

pygame.init()
screen = pygame.display.set_mode((720, 720), pygame.RESIZABLE)
pygame.display.set_caption("Point Line UI")
clock = pygame.time.Clock()
running = True

class Point:
    def __init__(self, x, y, theta = None):
        self.x = x
        self.y = y
        self.theta = theta
    def pos(self):
        return [self.x, self.y]
    def set_pos(self, x, y):
        self.x = x
        self.y = y
    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
    x: float
    y: float
    theta: float
class Line:
    def __init__(self, first_point, last_point):
        self.first_point = first_point    
        self.last_point = last_point
        self.carrot = Point(first_point.x + 50, first_point.y)
        self.carrot2 = Point(last_point.x + 50, last_point.y)
    
BG = (30, 30, 34)
LINE = (120, 180, 255)
DOT = (255, 255, 255)
HOVER = (255, 100, 100)
HEADING = (255, 200, 80)
HINT = (160, 160, 160)

points = []
lines = []
held_point = None
RADIUS = 6
INTERACTION_RADIUS = 20
FONT_SIZE = 14
FIELD_IMAGE = pygame.image.load("override.bmp")

while running:
    screenwidth = screen.get_width()
    screenheight = screen.get_height()
    field_image = pygame.transform.scale(
        FIELD_IMAGE, 
        (
            min(
                screenwidth, 
                screenheight - FONT_SIZE*2
            ),
        ) * 2 # this is not multiplying the number by two this is making it into a tuple with 2 of the same thingy
    ) # idc if this takes a shitton of space its more readable
    mousepos = pygame.mouse.get_pos()
    screen.fill(BG)
    screen.blit(field_image, (screen.get_width() / 2 - field_image.get_width() / 2, FONT_SIZE*2))    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSLASH] and points:
            points.pop()
        elif keys[pygame.K_c]:
            points.clear()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if keys[pygame.K_LSHIFT]:
                points.append(Point(event.pos[0], event.pos[1], 0.0))
                print(len(points))
                if len(points) > 1:
                    lines.append(Line(points[len(points)-2], points[len(points)-1]))
            else:
                for p in points:
                    if math.dist(mousepos, p.pos()) <= INTERACTION_RADIUS:
                        held_point = p
                for line in lines:
                    if math.dist(mousepos, line.carrot.pos()) <= INTERACTION_RADIUS:
                        held_point = line.carrot
                    elif math.dist(mousepos, line.carrot2.pos()) <= INTERACTION_RADIUS:
                        held_point = line.carrot2
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if held_point: 
                held_point = None
        elif event.type == pygame.MOUSEWHEEL:
            for p in points:
                if math.dist(mousepos, p.pos()) <= INTERACTION_RADIUS:
                    p.theta = (p.theta + event.y * 5) % 360
    
    if held_point != None:
        held_point.set_pos(mousepos)

    # lines = []
    # for i, p in enumerate(points[:-1]):
    #     pygame.draw.circle(screen, (255,0,0), p.pos(), 20)
    #     lines.append(Line(p, points[i+1]))
    
    
    for line in lines:
        p1 = line.first_point
        p2 = line.last_point
        c = line.carrot
        c2 = line.carrot2
        # dist = math.dist(p1.pos(), p2.pos())
        # LEAD = 0.5
        # line.carrot = Point(
        #     p1.x - (dist * math.sin(math.radians(p1.theta)) * LEAD),
        #     p1.y - (dist * math.cos(math.radians(p1.theta)) * LEAD),
        #     None
        # )
        # c = line.carrot
        # line.carrot2 = Point(
        #     p2.x - (dist * math.sin(math.radians(p2.theta)) * LEAD),
        #     p2.y - (dist * math.cos(math.radians(p2.theta)) * LEAD),
        #     None
        # )
        # c2 = line.carrot2
        pygame.draw.circle(screen, DOT, c.pos(), RADIUS)
        pygame.draw.circle(screen, DOT, c2.pos(), RADIUS)
        linepoints = []
        for t in [n * 0.01 for n in range(101)]:
            a = 1-t
            linepoints.append((
                p1.x * (a**3) + # a³x₁
                3 * (a**2) * t * c.x + # 3a²bc₁
                3 * a * (t**2) * c2.x + # 3ab²c₂
                (t**3) * p2.x, # b³x₂
                
                (a**3) * p1.y + 
                3 * (a**2) * t * c.y + 
                3 * a * (t**2) * c2.y + 
                (t**3) * p2.y
            ))
        pygame.draw.aalines(screen, (255,255,255), False, linepoints)

    # draw heading lines
    for p in points:
        rad = math.radians(p.theta)
        hx = p.x + math.sin(rad) * 25
        hy = p.y + math.cos(rad) * 25
        pygame.draw.line(screen, HEADING, p.pos(), (hx, hy), 2)

    # draw p dots
    for p in points:
        pygame.draw.circle(screen, DOT, p.pos(), RADIUS)

    # draw lines b/w dots and mousepos when shift held
    if len(points) > 1: pygame.draw.aalines(screen, LINE, False, [p.pos() for p in points])
    if len(points) > 0 and keys[pygame.K_LSHIFT]:
        pygame.draw.aalines(screen, LINE, False, [p.pos() for p in points] + [mousepos])


    # draw keybinds
    font = pygame.font.SysFont("monospace", FONT_SIZE)
    hint = font.render("shift+click: add point   backspace: undo   c: clear   scroll: rotate theta", True, HINT)
    screen.blit(hint, (12, 8))



    pygame.display.flip()
    clock.tick(60)

pygame.quit()
