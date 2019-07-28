if __name__ == 'classes.Eye':

    from settings import SIZE
    from utils import angle_calc

    from classes.PickUp import PickUp
    from classes.EyeServant import EyeServant

    import pygame
    from math import sqrt
    from random import randint, uniform


    class Eye:
        move = 1
        hp = 55

        def __init__(self, x, y):
            # --Настройки--
            self.Max_Speed = 5
            self.hp = Eye.hp
            # -------------
            self.x, self.y = x, y
            self.texture0 = pygame.image.load(r'data\textures\eye.png').subsurface(0, 0, 152, 110).convert()
            self.texture1 = pygame.image.load(r'data\textures\eye.png').subsurface(152, 0, 136, 110).convert()
            self.image = self._image = self.texture0
            self.rect = self.image.get_rect()
            self.angle = 0
            self.attack = False
            self.Visible = False
            self.cooldown = self.cooldown0 = 250
            self.distance = 0
            self.aim = [0, 0]
            self.distance_min = 250
            self.dx = self.dy = 0

        def render(self, game):
            # Движение к цели
            self.aim = game.hero.rect.center
            self.distance = sqrt(pow(self.aim[0] - self.x, 2) + pow(self.aim[1] - self.y, 2))

            if self.distance >= Eye.move:
                self.dx += ((self.aim[0] - self.x) / self.distance) * Eye.move
                self.dy += ((self.aim[1] - self.y) / self.distance) * Eye.move
            else:
                self.dx += self.aim[0] - self.x
                self.dy += self.aim[1] - self.y

            # Соблюдение дистанции
            if sqrt(pow(self.aim[0] - self.x + self.dx, 2) + pow(self.aim[1] - self.y, 2)) <= self.distance_min:
                self.dx -= ((self.aim[0] - self.x) / self.distance) * (Eye.move + 0.5)

            if sqrt(pow(self.aim[0] - self.x, 2) + pow(self.aim[1] - self.y + self.dy, 2)) <= self.distance_min:
                self.dy -= ((self.aim[1] - self.y) / self.distance) * (Eye.move + 0.5)

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

            if self.hp > 30:
                if self.attack:
                    self.image = self.texture1
                    self.Max_Speed = 8
                else:
                    self.image = self.texture0
                    self.Max_Speed = 5
            else:
                if self.attack:
                    self.Max_Speed = 10
                else:
                    self.Max_Speed = 8
                self.image = self.texture1

            if self.attack:
                if self.rect.colliderect(game.hero.rect):
                    if self.hp > 30:
                        game.hero.hp -= 2
                        game.hero.dx += self.dx
                        game.hero.dy += self.dy
                    else:
                        game.hero.hp -= 4
                        game.hero.dx += self.dx * 1.5
                        game.hero.dy += self.dy * 1.5

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
                    game.enemy.append(EyeServant(uniform(self.x - 20, self.x + 20), uniform(self.y - 20, self.y + 20),
                                            uniform(-10, 10), uniform(-10, 10)))
                    game.pickup.append(PickUp(randint(round(self.x) - 50, round(self.x) + 50),
                                         randint(round(self.y) - 50, round(self.y) + 50), 'diamond'))
                game.enemy.remove(self)

            if (game.camera.x - 180 < self.rect.x < game.camera.x + SIZE[0] + 10) and \
                    (game.camera.y - 180 < self.rect.y < game.camera.y + SIZE[1] + 20):
                self.Visible = True
                # Угол наклона картинки
                self.angle = angle_calc(*self.aim, self.x, self.y)
                self._image = pygame.transform.rotate(self.image, self.angle)

                self.draw(game)

            else:
                self.Visible = False

            # Движение
            self.x += self.dx
            self.y += self.dy

            self.rect.width = self._image.get_width()
            self.rect.height = self._image.get_height()
            self.rect.center = self.x, self.y

        def draw(self, game):
            game.screen.blit(self._image, game.camera.get_pos(self.rect.x, self.rect.y))
