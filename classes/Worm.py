if __name__ == 'classes.Worm':
    import pygame

    from settings import SIZE

    class Worm:
        move = 5
        hp = 10
        damage = 1

        def __init__(self, x, y):
            self.Max_Speed = 20
            self.x, self.y = x, y
            self.dy = self.dx = 0
            self.image = pygame.image.load(r'data\textures\worm.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.Visible = True
            self.direction_up = True

        def render(self, game):
            # Ограничение скорости
            if self.dy < -self.Max_Speed:
                self.dy = -self.Max_Speed

            # Движение
            if self.direction_up:
                self.dy -= Worm.move
            else:
                self.dy += Worm.move
            self.y += self.dy
            self.rect.center = self.x, self.y

            # Атака
            if self.direction_up and self.rect.colliderect(game.hero.rect):
                game.hero.hp -= Worm.damage
                game.hero.dy -= 10
                self.direction_up = False

            if self.rect.y < game.hero.rect.y:
                self.direction_up = False

            # Выход за границы видимости
            if not self.direction_up:
                pos = game.camera.get_pos(self.x, self.y)

                if not((pos[0] in range(-34, SIZE[0] + 10)) and (pos[1] in range(-34, SIZE[1] + 450))):
                    self.hp = 0

            # Отображение
            self.draw(game)

            # Жизни юнита
            if self.hp <= 0:
                game.enemy.remove(self)

        def draw(self, game):
            game.screen.blit(self.image, game.camera.get_pos(self.x - self.image.get_width() / 2,
                                                             self.y - self.image.get_height() / 2))

