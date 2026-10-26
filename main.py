import pygame
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Point Line UI")
clock = pygame.time.Clock()
running = True

BG = (30, 30, 34)
LINE = (120, 180, 255)
DOT = (255, 255, 255)
HOVER = (255, 100, 100)
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
                points.append(event.pos)
            else:
                for i, p in enumerate(points):
                    if math.dist(mousepos, p) <= INTERACTION_RADIUS:
                        held_point = i
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if held_point: 
                held_point = None
    
    if held_point != None:
        points[held_point] = mousepos

    
    
    
    # draw lines b/w points
    if len(points) > 1:
            pygame.draw.lines(screen, LINE, False, points, 3)
            
    # draw p dots
    for p in points:
        pygame.draw.circle(screen, DOT, p, RADIUS)

    # draw lines b/w dots and mousepos
    if len(points) > 0 and keys[pygame.K_LSHIFT]:
        pygame.draw.aalines(screen, LINE, False, points + [mousepos])


    # draw keybinds
    font = pygame.font.SysFont("monospace", 14)
    hint = font.render("shift+click: add point   backspace: undo   c: clear   tab: swap type", True, HINT)
    screen.blit(hint, (12, 8))



    pygame.display.flip()
    clock.tick(60)

pygame.quit()
