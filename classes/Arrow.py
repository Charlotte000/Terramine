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
            self.freeze = False

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
                if not self.freeze:
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
            animal_list = [item for sublist in game.animals.values() for item in sublist if item.Visible]
            collide_objects = [n for n in game.block if n.Visible and n.Collision] + \
                              [en for en in game.enemy if en.Visible] + \
                              animal_list

            for n in pygame.Rect.collidelistall(self.rect, collide_objects):
                if collide_objects[n] in game.block:
                    self.freeze = True
                    self.dx = self.dy = 0
                    self.countdown -= 1
                    break
                elif collide_objects[n] in animal_list:
                    collide_objects[n].hp -= Arrow.damage
                    if self.dx > 0:
                        collide_objects[n].dx += 15
                    elif self.dx < 0:
                        collide_objects[n].dx -= 15
                    collide_objects[n].dy -= 5
                    self.x = -50
                    break
                elif collide_objects[n] in game.enemy:
                    collide_objects[n].hp -= Arrow.damage
                    if type(collide_objects[n]) not in [Eye, Cthulhu, Worm]:
                        if self.dx > 0:
                            collide_objects[n].dx += 15
                        elif self.dx < 0:
                            collide_objects[n].dx -= 15
                        collide_objects[n].dy -= 5
                    self.x = -50
                    break
