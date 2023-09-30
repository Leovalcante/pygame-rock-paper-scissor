import pygame

from network import Network
from model import Player

width = 500
height = 500

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rock Paper Scissor Desktop Client")


def redraw_window(win, player, player2):
    win.fill((255, 255, 255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    p = n.get_p()
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)

        p2 = n.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        p.move()
        redraw_window(window, p, p2)

    pygame.quit()


if __name__ == "__main__":
    main()
