import pygame

from network import Network

width = 700
height = 700

window = pygame.display.set_mode((width, height))
pygame.font.init()
pygame.display.set_caption("Rock Paper Scissor Desktop Client")


class Color:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)


font_family = "Roboto"
font_antialias = True


class Button:
    def __init__(self, text, x, y, color) -> None:
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont(font_family, 40)
        text = font.render(self.text, font_antialias, Color.white)
        win.blit(
            text,
            (
                self.x + round(self.width / 2) - round(text.get_width() / 2),
                self.y + round(self.height / 2) - round(text.get_height() / 2),
            ),
        )

    def click(self, pos):
        x, y = pos
        return (
            self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
        )


def redraw_window(win, game, p):
    win.fill(Color.white)
    if not game.connected():
        font = pygame.font.SysFont(font_family, 80)
        text = font.render("Waiting for player", 1, Color.red)
        win.blit(
            text,
            (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2),
        )
    else:
        font = pygame.font.SysFont(font_family, 60)
        text = font.render("Your move", font_antialias, Color.black)
        win.blit(text, (80, 200))

        text = font.render("Opponent move", font_antialias, Color.black)
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.both_went():
            text1 = font.render(move1, font_antialias, Color.black)
            text2 = font.render(move2, font_antialias, Color.black)
        else:
            if game.p1went and p == 0:
                text1 = font.render(move1, font_antialias, Color.black)
            elif game.p1went:
                text1 = font.render("Locked in", font_antialias, Color.black)
            else:
                text1 = font.render("Waiting...", font_antialias, Color.black)

            if game.p2went and p == 1:
                text2 = font.render(move2, font_antialias, Color.black)
            elif game.p2went:
                text2 = font.render("Locked in", font_antialias, Color.black)
            else:
                text2 = font.render("Waiting...", font_antialias, Color.black)

            if p == 1:
                win.blit(text2, (100, 350))
                win.blit(text1, (400, 350))
            else:
                win.blit(text1, (100, 350))
                win.blit(text2, (400, 350))
        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [
    Button("Rock", 50, 500, Color.red),
    Button("Paper", 250, 500, Color.green),
    Button("Scissor", 450, 500, Color.blue),
]


def main():
    run = True
    clock = pygame.time.Clock()

    n = Network()
    player = int(n.get_p())
    print(f"[+] Connected as player {player}")

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
            print(game.moves)
        except:
            run = False
            print(f"[!] Got error: couldn't get game")
            break

        if game.both_went():
            redraw_window(window, game, player)
            pygame.time.delay(500)
            try:
                n.send("reset")
            except:
                run = False
                print(f"[!] Got error: couldn't get game")
                break

            font = pygame.font.SysFont(font_family, 90)
            if game.winner() == player:
                text = font.render("You won!", font_antialias, Color.red)
            elif game.winner() == -1:
                text = font.render("Tie game!", font_antialias, Color.red)
            else:
                text = font.render("You lost...", font_antialias, Color.red)

            window.blit(
                text,
                (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2),
            )
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1went:
                                n.send(btn.text)
                        else:
                            if not game.p2went:
                                n.send(btn.text)

        redraw_window(window, game, player)


if __name__ == "__main__":
    main()
