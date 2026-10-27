import pygame
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Point Line UI")
clock = pygame.time.Clock()
running = True

class Point:
    def __init__(self, x, y, theta):
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

BG = (30, 30, 34)
LINE = (120, 180, 255)
DOT = (255, 255, 255)
HOVER = (255, 100, 100)
HEADING = (255, 200, 80)
HINT = (160, 160, 160)

points = []
held_point = None
RADIUS = 6
INTERACTION_RADIUS = 20
while running:
    mousepos = pygame.mouse.get_pos()
    screen.fill(BG)
    
    
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
            else:
                for i, p in enumerate(points):
                    if math.dist(mousepos, p.pos()) <= INTERACTION_RADIUS:
                        held_point = i
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if held_point: 
                held_point = None
        elif event.type == pygame.MOUSEWHEEL:
            for p in points:
                if math.dist(mousepos, p.pos()) <= INTERACTION_RADIUS:
                    p.theta = (p.theta + event.y * 5) % 360
    
    if held_point != None:
        points[held_point].set_pos(mousepos)

    
    
    
    # draw lines b/w points
    if len(points) > 1:
            pygame.draw.lines(screen, LINE, False, [p.pos() for p in points], 3)

    # draw heading lines
    for p in points:
        rad = math.radians(p.theta)
        hx = p.x + math.cos(rad) * 25
        hy = p.y + math.sin(rad) * 25
        pygame.draw.line(screen, HEADING, p.pos(), (hx, hy), 2)

    # draw p dots
    for p in points:
        pygame.draw.circle(screen, DOT, p.pos(), RADIUS)

    # draw lines b/w dots and mousepos
    if len(points) > 0 and keys[pygame.K_LSHIFT]:
        pygame.draw.aalines(screen, LINE, False, [p.pos() for p in points] + [mousepos])


    # draw keybinds
    font = pygame.font.SysFont("monospace", 14)
    hint = font.render("shift+click: add point   backspace: undo   c: clear   scroll: rotate theta", True, HINT)
    screen.blit(hint, (12, 8))



    pygame.display.flip()
    clock.tick(60)

pygame.quit()
