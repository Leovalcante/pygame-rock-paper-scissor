import pygame

from network import Network


# Client vars
window_width = 700
window_height = 700
font_family = "Roboto"
font_antialias = True


class Color:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)


class FontSize:
    sm = 40
    md = 60
    lg = 80
    xl = 90


# PyGame initializations
window = pygame.display.set_mode((window_width, window_height))
pygame.font.init()
pygame.display.set_caption("Rock Paper Scissor Desktop Client")


# Client buttons
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
        font = pygame.font.SysFont(font_family, FontSize.sm)
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


btns = [
    Button("Rock", 50, 500, Color.red),
    Button("Paper", 250, 500, Color.green),
    Button("Scissor", 450, 500, Color.blue),
]


# Manage client window
def redraw_window(win, game, p):
    win.fill(Color.white)
    if not game.connected():
        font = pygame.font.SysFont(font_family, FontSize.lg)
        text = font.render("Waiting for player", font_antialias, Color.red)
        win.blit(
            text,
            (
                window_width / 2 - text.get_width() / 2,
                window_height / 2 - text.get_height() / 2,
            ),
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
            msg1 = move1
            msg2 = move2
        else:
            if game.p1went and p == 0:
                msg1 = move1
            elif game.p1went:
                msg1 = "Locked in"
            else:
                msg1 = "Waiting..."

            if game.p2went and p == 1:
                msg2 = move2
            elif game.p2went:
                msg2 = "Locked in"
            else:
                msg2 = "Waiting..."

        text1 = font.render(msg1, font_antialias, Color.black)
        text2 = font.render(msg2, font_antialias, Color.black)

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


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
            # print(game.moves)  # uncomment this to cheat with your friends ;)
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

            font = pygame.font.SysFont(font_family, FontSize.xl)
            if game.winner() == player:
                msg = "You won!"
            elif game.winner() == -1:
                msg = "Tie game!"
            else:
                msg = "You lost..."

            text = font.render(msg, font_antialias, Color.red)
            window.blit(
                text,
                (
                    window_width / 2 - text.get_width() / 2,
                    window_height / 2 - text.get_height() / 2,
                ),
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
