if __name__ == 'classes.Cthulhu':

    from settings import SIZE

    from classes.PickUp import PickUp
    from classes.Worm import Worm

    import pygame
    from pyganim import PygAnimation
    from math import sqrt
    from random import randint

    class Cthulhu:
        move = .1
        hp = 100

        def __init__(self, x, y):
            # --Настройки--
            self.Max_Speed = 1
            self.hp = Cthulhu.hp
            # -------------
            self.x, self.y = x, y
            self.dx = self.dy = 0

            # Creating animation
            resource = pygame.image.load(r'data\textures\cthulhu.png').convert_alpha()
            frames = [
                [resource.subsurface(resource.get_width() // 8 * x, resource.get_height() // 3 * y,
                                     resource.get_width() // 8, resource.get_height() // 3), 100]
                for y in range(0, 3) for x in range(0, 8)
            ]

            self.anim_walk = PygAnimation(frames[:8])
            self.anim_rotate = PygAnimation(frames[16:18] + frames[20:21] + frames[18:20])
            self.anim_attack = PygAnimation(frames[8:16])
            self.anim_walk.play()
            self.anim_rotate.play()
            self.anim_attack.play()

            self.anim_l = False
            self.rotating = False

            self.rect = self.anim_walk.getRect()
            self.attack = False
            self.Visible = False
            self.throw_worms = False
            self.cooldown = self.cooldown0 = 250
            self.distance = 0
            self.aim = [0, 0]
            self.zombie_count = 10
            self.distance_min = 250

        def render(self, game):
            # Движение к цели
            self.aim = game.hero.rect.center

            if self.rect.centery < self.aim[1] - Cthulhu.move:
                self.dy += Cthulhu.move
            elif self.rect.centery > self.aim[1] + Cthulhu.move:
                self.dy -= Cthulhu.move

            if self.rect.centerx < self.aim[0]:
                if self.anim_l:
                    self.rotating = True
                self.anim_l = False
                self.dx += Cthulhu.move
            elif self.rect.centerx > self.aim[0]:
                if not self.anim_l:
                    self.rotating = True
                self.anim_l = True
                self.dx -= Cthulhu.move

            # Соблюдение дистанции
            self.distance = sqrt(pow(self.aim[0] - self.x, 2) + pow(self.aim[1] - self.y, 2))
            if self.distance <= self.distance_min:
                if self.anim_l:
                    self.dx += Cthulhu.move * 10
                else:
                    self.dx -= Cthulhu.move * 10

            # Контроль скорости
            if self.dx > self.Max_Speed:
                self.dx = self.Max_Speed
            elif self.dx < -self.Max_Speed:
                self.dx = -self.Max_Speed

            if self.dy > self.Max_Speed:
                self.dy = self.Max_Speed
            elif self.dy < -self.Max_Speed:
                self.dy = -self.Max_Speed

            # Атака
            if self.attack:
                self.distance_min = 60
            else:
                self.distance_min = 250

            if self.hp > 50:
                if 1 == randint(1, 200):
                    game.enemy.append(Worm(game.hero.rect.centerx, game.hero.rect.centery + SIZE[1]))
                if self.attack:
                    self.Max_Speed = 5
                else:
                    self.Max_Speed = 3
            else:
                if not self.throw_worms:
                    i = 0
                    for x in range(round(self.x), round(self.x + 500), 60):
                        game.enemy.append(Worm(x, game.hero.rect.centery + SIZE[1] + i * 100))
                        i += 1
                    i = 0
                    for x in range(round(self.x), round(self.x - 500), -60):
                        game.enemy.append(Worm(x, game.hero.rect.centery + SIZE[1] + i * 100))
                        i += 1
                    game.time = 180
                    self.throw_worms = True

                if 1 == randint(1, 50):
                    game.enemy.append(Worm(game.hero.rect.centerx, game.hero.rect.centery + SIZE[1]))
                if self.zombie_count > 0:
                    if 1 == randint(1, 40):
                        self.zombie_count -= 1
                        game.add_zombie()
                if self.attack:
                    self.Max_Speed = 7
                else:
                    self.Max_Speed = 5

            if self.attack:
                if self.rect.colliderect(game.hero.rect):
                    if self.hp > 50:
                        game.hero.hp -= 2
                        game.hero.dx += self.dx * 5
                        game.hero.dy -= self.dy * 5
                    else:
                        game.hero.hp -= 4
                        game.hero.dx += self.dx * 7
                        game.hero.dy -= self.dy * 7

                    self.attack = False

            if self.cooldown0 <= self.cooldown:
                self.cooldown0 -= 1

            if self.cooldown0 <= 0:
                self.attack = True
                if self.hp > 30:
                    self.cooldown = randint(100, 250)
                else:
                    self.cooldown = randint(30, 100)
                self.cooldown0 = self.cooldown

            # Жизни юнита
            if self.hp <= 0:

                for n in range(0, 12):
                    game.pickup.append(PickUp(randint(round(self.rect.centerx) - 50, round(self.rect.centerx) + 50),
                                         randint(round(self.rect.centery) - 50, round(self.rect.centery) + 50),
                                              'diamond'))

                game.enemy.remove(self)

            if (game.camera.x - 70 < self.rect.x < game.camera.x + SIZE[0] + 10) and \
                    (game.camera.y - 100 < self.rect.y < game.camera.y + SIZE[1] + 20):
                self.Visible = True
                self.draw(game)

            else:
                self.Visible = False

            # Движение
            self.x += self.dx
            self.y += self.dy

            self.rect.center = self.x, self.y

        def draw(self, game):
            if self.rotating:
                if self.anim_l:
                    game.screen.blit(pygame.transform.flip(self.anim_rotate.getCurrentFrame(), True, False),
                                     game.camera.get_pos(self.x - self.rect.w / 2, self.y - self.rect.h / 2))
                else:
                    self.anim_rotate.blit(game.screen,
                                          game.camera.get_pos(self.x - self.rect.w / 2, self.y - self.rect.h / 2))
            else:
                if self.anim_l:
                    if self.attack:
                        game.screen.blit(pygame.transform.flip(self.anim_attack.getCurrentFrame(), True, False),
                                         game.camera.get_pos(self.x - self.rect.w / 2, self.y - self.rect.h / 2))
                    else:
                        game.screen.blit(pygame.transform.flip(self.anim_walk.getCurrentFrame(), True, False),
                                         game.camera.get_pos(self.x - self.rect.w / 2, self.y - self.rect.h / 2))
                else:
                    if self.attack:
                        self.anim_attack.blit(game.screen,
                                              game.camera.get_pos(self.x - self.rect.w / 2, self.y - self.rect.h / 2))
                    else:
                        self.anim_walk.blit(game.screen,
                                            game.camera.get_pos(self.x - self.rect.w / 2, self.y - self.rect.h / 2))

            if self.anim_rotate.currentFrameNum == self.anim_rotate.numFrames - 1:
                self.rotating = False
