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
            print("qui?")
            return getattr(current_module, name)
        # Forbid everything else
        raise pickle.UnpicklingError(f"Cannot unpickle {module}.{name}")
