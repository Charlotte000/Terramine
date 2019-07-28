if __name__ == 'classes.Bird':

    from settings import SIZE
    from classes.PickUp import PickUp

    import pygame
    from pyganim import PygAnimation
    from random import randint


    class Bird:
        def __init__(self, x, y, direction_left):
            # -Настройки-
            self.dx = 10
            self.dy = 0
            self.hp = 0.5
            # -----------
            if direction_left:
                self.dx *= -1

            self.x, self.y = x, y
            self.Visible = True
            self.rect = pygame.Rect(x, y, 45, 59)

            image = pygame.image.load(r'data\textures\bird.png').convert_alpha()
            frames = []
            if direction_left is False:
                image = pygame.transform.flip(image, True, False)
            for x in range(0, 22):
                frames.append([image.subsurface(x * 45, 0, 45, 59), 50])
            self.anim_left = PygAnimation(frames)
            self.anim_left.play()

        def render(self, game):
            # Перемещение
            self.x += self.dx
            self.rect.center = self.x, self.y

            if abs(self.x - game.hero.x) >= SIZE[0] * 12:
                # Границы существования
                game.animals['bird'].remove(self)
            else:
                self.Visible = False
                if (game.camera.x - 45 < self.rect.x < game.camera.x + SIZE[0] + 5) and \
                        (game.camera.y - 59 < self.rect.y < game.camera.y + SIZE[1] + 5):
                    self.Visible = True

                    # Количество жизней
                    if self.hp <= 0:
                        for count in range(1, randint(2, 4)):
                            game.pickup.append(PickUp(self.x - randint(-10, 10), self.y, 'fowl'))
                        game.animals['bird'].remove(self)
                    self.draw(game)

        def draw(self, game):
            self.anim_left.blit(game.screen, game.camera.get_pos(self.rect.x, self.rect.y))
