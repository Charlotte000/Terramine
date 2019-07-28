if __name__ == 'classes.Arrow':

    from data.textures.loader import i_arrow
    from settings import SIZE
    from utils import angle_calc

    from classes.Eye import Eye
    from classes.Cthulhu import Cthulhu
    from classes.Worm import Worm

    from math import sqrt
    import pygame


    class Arrow:
        gravity = 1
        move = 25
        damage = 1
        countdown = 500

        def __init__(self, x, y, x1, y1):
            self.x, self.y = x, y
            self.aim = x1, y1

            r = sqrt(pow(self.aim[0] - self.x, 2) + pow(self.aim[1] - self.y, 2))

            if r > 0:
                if r >= Arrow.move:
                    self.dx = ((self.aim[0] - self.x) / r) * Arrow.move
                    self.dy = ((self.aim[1] - self.y) / r) * Arrow.move
                else:
                    self.dx = self.aim[0] - self.x
                    self.dy = self.aim[1] - self.y
            else:
                self.dx = self.dy = 0
            self.image = self.image0 = i_arrow.subsurface(0, 7, 20, 6)
            self.angle = 0
            self.rect = self.image0.get_rect()
            self.rect.center = x, y
            self.countdown = Arrow.countdown

        def render(self, game):
            if (game.camera.x - 20 < self.rect.x < game.camera.x + SIZE[0] + 5) and \
                    (game.camera.y - 20 < self.rect.y < game.camera.y + SIZE[1] + 5):
                # Гравитация
                if self.dx != 0 or self.dy != 0:
                    self.dy += Arrow.gravity

                    # Поворот картинки
                    self.angle = angle_calc(self.dx, self.dy, 0, 0)
                    self.image0 = pygame.transform.rotate(self.image, self.angle)

                    # Перемещение
                    self.x += self.dx
                    self.y += self.dy
                    self.rect.center = self.x, self.y
                    self.rect.size = self.image0.get_size()
                    self.collision(game)

                self.draw(game)
            else:
                game.arrow.remove(self)

            # Исченовение
            if self.countdown < Arrow.countdown:
                self.countdown -= 1
            if self.countdown <= 0:
                self.rect.x = -50

        def draw(self, game):
            game.screen.blit(self.image0, game.camera.get_pos(self.rect.x, self.rect.y))

        def collision(self, game):
            for cube in game.block:
                if cube.Visible and cube.Collision:
                    if pygame.sprite.collide_rect(self, cube):
                        self.dx = self.dy = 0
                        self.countdown -= 1
                        break
            for types in game.animals:
                for unit in game.animals[types]:
                    if unit.Visible:
                        if pygame.sprite.collide_rect(self, unit):
                            unit.hp -= Arrow.damage
                            if self.dx > 0:
                                unit.dx += 15
                            elif self.dx < 0:
                                unit.dx -= 15
                            unit.dy -= 5
                            self.x = -50
                            break
            for unit in game.enemy:
                if unit.Visible:
                    if pygame.sprite.collide_rect(self, unit):
                        unit.hp -= Arrow.damage
                        if type(unit) not in [Eye, Cthulhu, Worm]:
                            if self.dx > 0:
                                unit.dx += 15
                            elif self.dx < 0:
                                unit.dx -= 15
                            unit.dy -= 5
                        self.x = -50
                        break
