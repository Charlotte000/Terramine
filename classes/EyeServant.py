if __name__ == 'classes.EyeServant':

    from settings import SIZE
    from utils import angle_calc

    import pygame
    from math import sqrt
    from random import randint, uniform


    class EyeServant:
        move = 1

        def __init__(self, x, y, dx=0, dy=0):
            # --Настройки--
            self.Max_Speed = 5
            self.hp = 2
            # -------------
            self.x, self.y = x, y
            self.image = self._image = pygame.image.load(r'data\textures\eye_servant.png').convert()
            self.rect = self.image.get_rect()
            self.angle = 0
            self.attack = False
            self.Visible = True
            self.cooldown = self.cooldown0 = randint(30, 250)
            self.distance = 0
            self.aim = [0, 0]
            self.distance_min = randint(100, 250)
            self.dx, self.dy = dx, dy

        def render(self, game):
            # Движение к цели
            self.aim = game.hero.rect.center
            self.distance = sqrt(pow(self.aim[0] - self.x, 2) + pow(self.aim[1] - self.y, 2))

            if self.distance >= EyeServant.move:
                self.dx += ((self.aim[0] - self.x) / self.distance) * uniform(0, EyeServant.move)
                self.dy += ((self.aim[1] - self.y) / self.distance) * uniform(0, EyeServant.move)
            else:
                self.dx += self.aim[0] - self.x
                self.dy += self.aim[1] - self.y

            # Соблюдение дистанции
            if sqrt(pow(self.aim[0] - self.x + self.dx, 2) + pow(self.aim[1] - self.y, 2)) <= self.distance_min:
                self.dx -= ((self.aim[0] - self.x) / self.distance) * (EyeServant.move + 0.5)

            if sqrt(pow(self.aim[0] - self.x, 2) + pow(self.aim[1] - self.y + self.dy, 2)) <= self.distance_min:
                self.dy -= ((self.aim[1] - self.y) / self.distance) * (EyeServant.move + 0.5)

            # Контроль скорости
            if self.dx > self.Max_Speed:
                self.dx -= EyeServant.move
            elif self.dx < -self.Max_Speed:
                self.dx += EyeServant.move

            if self.dy > self.Max_Speed:
                self.dy -= EyeServant.move
            elif self.dy < -self.Max_Speed:
                self.dy += EyeServant.move

            # Атака
            if self.attack:
                self.distance_min = 60
            else:
                self.distance_min = randint(100, 250)

            if self.attack:
                self.Max_Speed = 8
                if self.rect.colliderect(game.hero.rect):
                    game.hero.hp -= 1
                    game.hero.dx += self.dx * 0.5
                    game.hero.dy += self.dy * 0.5
                    self.attack = False
            else:
                self.Max_Speed = 5

            if self.cooldown0 <= self.cooldown:
                self.cooldown0 -= 1

            if self.cooldown0 <= 0:
                self.attack = True
                self.cooldown = randint(30, 250)

                self.cooldown0 = self.cooldown

            # Жизни юнита
            if self.hp <= 0:
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
