import inspect
import pickle
import sys

import pygame


class Player:
    def __init__(self, x, y, width, height, color) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 1

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


class Game:
    def __init__(self, id_) -> None:
        self.p1went = False
        self.p2went = False
        self.ready = False
        self.id = id_
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    def get_player_move(self, p):
        return self.moves[p]

    def play(self, p, move):
        self.moves[p] = move
        if p == 0:
            self.p1went = True
        else:
            self.p2went = True

    def connected(self):
        return self.ready

    def both_went(self):
        return self.p1went and self.p2went

    def winner(self):
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        if p1 == p2:
            return -1

        win_con = ["R", "P", "S"]
        if win_con[win_con.index(p1) - 1] == p2:
            return 0

        return 1

    def reset(self):
        self.p1went = False
        self.p2went = False


# !!! This shoud be left down here in the following order !!!
# This will load any class in the current module except the one below this code
# The `safe_classes` list is then used to verify which classes can be
# deserialized via `pickle.loads`
current_module = sys.modules[__name__]
safe_classes = {
    klass_tuple[0]
    for klass_tuple in inspect.getmembers(
        current_module,
        lambda member: inspect.isclass(member) and member.__module__ == __name__,
    )
}


class SafeUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Only allow safe classes
        if module == current_module.__name__ and name in safe_classes:
            return getattr(current_module, name)
        # Forbid everything else
        raise pickle.UnpicklingError(f"Cannot unpickle {module}.{name}")
