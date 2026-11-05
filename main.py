"""
TODO:
- make it so that the cubic bezier is a class that inherits from Line
- also re-add ability to do quadratic bezier
- fix carrot point thin
- rename carrot to control point
- make theta follow control point 
""" 


import pygame
import json
import math

pygame.init()
screen = pygame.display.set_mode((720, 720), pygame.RESIZABLE)
pygame.display.set_caption("rts")
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
        self.p1 = first_point    
        self.p2 = last_point
        

class Bezier(Line):
    def __init__(self, first_point, last_point, c=None, c2=None):
        super().__init__(first_point, last_point)
        if c: self.c = c 
        else: self.c = Point(first_point.x + 50, first_point.y)
        if c2: self.c2 = c2
        else: self.c2 = Point(last_point.x + 50, last_point.y)
    
    def calculate(self, t):
        a = 1-t
        return (
            self.p1.x * (a**3) +
            3 * (a**2) * t * self.c.x +
            3 * a * (t**2) * self.c2.x +
            (t**3) * self.p2.x,
            
            (a**3) * self.p1.y + 
            3 * (a**2) * t * self.c.y + 
            3 * a * (t**2) * self.c2.y + 
            (t**3) * self.p2.y
        )
    def derivative(self, t, h=1e-3):
        x, y = self.calculate(t)
        x1, y1 = self.calculate(min(t+h,1))
        return(
            (x1 - x) / h,
            (y1 - y) / h
        )
    def double_derivative(self, t, h=1e-3):
        dx, dy = self.derivative(max(t-h,0), h)
        dx1, dy1 = self.derivative(min(t+h,1), h)
        return(
            (dx1 - dx) / (2*h),
            (dy1 - dy) / (2*h)
        )
        
    def curvature(self, t):
        (dx, dy), (ddx, ddy) = self.derivative(t), self.double_derivative(t)
        return (abs(dx*ddy - dy*ddx) / (dx**2 + dy**2)**1.5) # i lowk dont get the numerator of this formula.. like i get the top part but the bottom is because of smth with vectors that i dont get



    
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
        if keys[pygame.K_s]:
            with open("path.json", "w") as file:
                
                # for line in lines:
                #     p1 = '{' + f'"x": "{line.p1.x}", "y": "{line.p1.y}"' + '}'
                #     p2 = '{' + f'"x": "{line.p2.x}", "y": "{line.p2.y}"' + '}'
                #     c1 = '{' + f'"x": "{line.c.x}", "y": "{line.c.y}"' + '}'
                #     c2 = '{' + f'"x": "{line.c2.x}", "y": "{line.c2.y}"' + '}'
                #     output += "{" + f'"p1":{p1}, "p2":{p2}, "c":{c1}, "c2":{c2}' + "}"
                #     if len(lines)-1 != lines.index(line): output += ","
                output = []
                for line in lines: output.append({"p1": (line.p1.x, line.p1.y), "p2": (line.p2.x, line.p2.y), "c": (line.c.x, line.c.y), "c2": (line.c2.x, line.c2.y)})
                file.write(json.dumps(output))
        if keys[pygame.K_o]:
            with open("path.json", "r") as file:
                lines.clear()
                points.clear()
                for line in json.loads(file.read()):
                    lines.append(
                        Bezier(
                            Point(line["p1"][0], line["p1"][1]),
                            Point(line["p2"][0], line["p2"][1]),
                            Point(line["c"][0], line["c"][1]),
                            Point(line["c2"][0], line["c2"][1]),
                        )
                    )
                    points.append(Point(line["p1"][0], line["p1"][1], 0))
                    points.append(Point(line["p2"][0], line["p2"][1], 0))
                    

        if keys[pygame.K_BACKSLASH] and points:
            points.pop()
        elif keys[pygame.K_c]:
            lines.clear()
            points.clear()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if keys[pygame.K_LSHIFT]:
                points.append(Point(event.pos[0], event.pos[1], 0.0))
                # print(len(points))
                if len(points) > 1:
                    lines.append(Bezier(points[len(points)-2], points[len(points)-1]))
            else:
                for p in points:
                    if math.dist(mousepos, p.pos()) <= INTERACTION_RADIUS:
                        held_point = p
                for line in lines:
                    if math.dist(mousepos, line.c.pos()) <= INTERACTION_RADIUS:
                        held_point = line.c
                    elif math.dist(mousepos, line.c2.pos()) <= INTERACTION_RADIUS:
                        held_point = line.c2
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
        p1 = line.p1
        p2 = line.p2
        c = line.c
        c2 = line.c2
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
        linepoints = [(p1.x, p1.y)]
        granularity = 0.01
        for t in [n * granularity for n in range(int(1/granularity))]:
            linepoints.append(line.calculate(t))
            curvature = line.curvature(t) * 10000
            # print(f'point {len(linepoints)} has curvature {curvature}')
            pygame.draw.circle(screen, (min(curvature, 255), (100 - min(curvature, 100)), 0), line.calculate(t), RADIUS)
        linepoints.append((p2.x, p2.y))
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
