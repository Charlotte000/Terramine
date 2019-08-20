if __name__ == 'classes.Pig':
    import pygame
    from random import choice, randint

    from settings import SIZE

    from math import sqrt

    from classes.PickUp import PickUp

    class Pig:
        gravity = 1
        jump = 8
        active_time = 300
        active_cooldown = 10000

        def __init__(self, x, y):
            # -Настройки-
            self.Move = 2
            self.hp = 3
            # -----------
            self.Ground = False
            self.to_jump = False
            self.dx = self.dy = 0
            self.active = Pig.active_time
            self.active_cooldown = 0
            self.direction = choice([-1, 1])
            self.image = pygame.image.load(r'data\textures\pig.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = x, y
            self.Visible = True

        def render(self, game):
            if abs(self.rect.x - game.hero.x) < SIZE[0] * 5:
                self.Visible = False

                pos = game.camera.get_pos(self.rect.x, self.rect.y)

                if (pos[0] in range(-self.rect.width, SIZE[0])) and (pos[1] in range(-self.rect.height, SIZE[1])):
                    self.Visible = True

                    # Движение & следование за приманкой
                    if pos[0] in range(0, SIZE[0] - 34):
                        if game.hero.inventory[game.hero.inventory_menu_pos - 1] and \
                                game.hero.inventory[game.hero.inventory_menu_pos - 1][0] == 'wheat_seed' and \
                                abs(self.rect.x - game.hero.x) <= 250:
                            if self.rect.x > game.hero.x + 25:
                                self.direction = -1
                            elif self.rect.x < game.hero.x - 25:
                                self.direction = 1
                        elif 1 == randint(1, 50):
                            self.direction = randint(-1, 1)
                        if self.to_jump:
                            self.dy -= Pig.jump
                            self.to_jump = False
                    else:
                        self.direction = 0
                    self.dx = self.Move * self.direction

                    # Гравитация
                    if self.Ground is False:
                        self.dy += Pig.gravity
                    else:
                        self.Ground = False

                    # Количество жизней
                    if self.hp != 5:
                        self.Move = 2.2
                    if self.hp <= 0:
                        for count in range(1, randint(2, 4)):
                            game.pickup.append(PickUp(self.rect.centerx - randint(-10, 10), self.rect.centery,
                                                      'porkchop'))
                        game.animals['pig'].remove(self)

                    # Перемещение
                    self.rect.y += self.dy
                    self.collision(0, self.dy, game.block)
                    self.rect.x += self.dx
                    self.collision(self.dx, 0, game.block)

                    # Кормление
                    if self.active < Pig.active_time:
                        self.active += 1

                        for an in game.animals['pig']:
                            if self != an and an.active < Pig.active_time:
                                if sqrt(pow(self.rect.x - an.rect.x, 2) + pow(self.rect.y - an.rect.y, 2)) <= 50:
                                    self.active = an.active = Pig.active_time
                                    self.active_cooldown = an.active_cooldown = 1
                                    game.animals['pig'].append(Pig(self.rect.x + 10, self.rect.y))
                                    game.animals['pig'][-1].active_cooldown = 1
                                    break

                        if self.active >= Pig.active_time:
                            self.active_cooldown += 1
                    if 0 < self.active_cooldown < Pig.active_cooldown:
                        self.active_cooldown += 1
                    if self.active_cooldown >= Pig.active_cooldown:
                        self.active_cooldown = 0

                    self.draw(game, pos)

        def draw(self, game, pos):
            if self.direction == -1:
                game.screen.blit(self.image, pos)
            else:
                game.screen.blit(pygame.transform.flip(self.image, True, False), pos)

        def collision(self, dx, dy, block):
            collide_objects = [n for n in block if n.Visible and (n.Collision or n.name == 'fence')]

            for n in pygame.Rect.collidelistall(self.rect, collide_objects):
                if dx:
                    if dx > 0:
                        self.rect.right = collide_objects[n].rect.left
                    elif dx < 0:
                        self.rect.left = collide_objects[n].rect.right
                    self.dx = 0
                    if collide_objects[n] in block and self.Ground:
                        self.to_jump = True
                        if collide_objects[n].name == "fence":
                            self.to_jump = False
                        else:
                            for unit in block:
                                if unit.Visible and unit.Collision and (collide_objects[n] != unit):
                                    if unit.rect.x == collide_objects[n].rect.x:
                                        if unit.rect.y == collide_objects[n].rect.y - 25:
                                            self.to_jump = False
                                            self.direction *= -1
                                            break
                if dy > 0:
                    self.rect.bottom = collide_objects[n].rect.top
                    self.dy = 0
                    if collide_objects[n] in block:
                        self.Ground = True
                elif dy < 0:
                    self.rect.top = collide_objects[n].rect.bottom
                    self.dy = 0
