if __name__ == 'classes.Zombie':

    from settings import SIZE

    from classes.PickUp import PickUp

    import pygame
    from pyganim import PygAnimation
    from random import randint


    class Zombie:
        move = 2
        gravity = 1
        jump = 8
        damage = 0.1

        def __init__(self, x, y):
            # -Настройки-
            self.hp = 5
            # -----------
            self.Ground = False
            self.move_left = False
            self.to_jump = False
            self.Visible = True
            self.dx = self.dy = 0

            resource = pygame.image.load(r'data\textures\zombie.png').convert_alpha()
            self.rect = pygame.Rect(x, y, 22, 38)

            self.anim_r = PygAnimation([[resource.subsurface(x * 22, 0, 22, 38), 50] for x in range(0, 9)])
            self.anim_r.play()
            self.anim_l = PygAnimation([[resource.subsurface(x * 22, 38, 22, 38), 50] for x in range(0, 9)])
            self.anim_l.play()

        def render(self, game):
            # Движение к цели
            if game.hero.x > self.rect.x:
                if self.dx + Zombie.move <= Zombie.move:
                    self.dx += Zombie.move
                else:
                    self.dx = Zombie.move
                self.move_left = False
            elif game.hero.x < self.rect.x:
                if self.dx - Zombie.move >= - Zombie.move:
                    self.dx -= Zombie.move
                else:
                    self.dx = -Zombie.move
                self.move_left = True
            if self.to_jump:
                self.dy -= Zombie.jump
                self.to_jump = False

            # Границы
            if abs(self.rect.x - game.hero.x) > SIZE[0] * 1.5 or abs(self.rect.y - game.hero.y) > SIZE[1] * 1.5:
                game.enemy.remove(self)

            # Гравитация
            if self.Ground is False:
                self.dy += Zombie.gravity
            else:
                self.Ground = False

            # Количество жизней
            if self.hp <= 0:
                rand_choice = randint(1, 100)
                if 1 == rand_choice:
                    game.pickup.append(PickUp(self.rect.centerx, self.rect.centery, 'mushroom'))
                if 2 == rand_choice:
                    game.pickup.append(PickUp(self.rect.centerx, self.rect.centery, 'bread'))
                if 3 == rand_choice:
                    game.pickup.append(PickUp(self.rect.centerx, self.rect.centery, 'iron_helmet'))
                if 4 == rand_choice:
                    game.pickup.append(PickUp(self.rect.centerx, self.rect.centery, 'wheat_seed'))
                if 5 == rand_choice:
                    game.pickup.append(PickUp(self.rect.centerx, self.rect.centery, 'bread'))
                if 6 == rand_choice:
                    game.pickup.append(PickUp(self.rect.centerx, self.rect.centery, 'iron_pickaxe'))
                del rand_choice

                game.enemy.remove(self)

            # Перемещение
            self.rect.y += self.dy
            self.collision(0, self.dy, game.block, game.hero)
            self.rect.x += self.dx
            self.collision(self.dx, 0, game.block, game.hero)

            if (game.camera.x - 22 < self.rect.x < game.camera.x + SIZE[0] + 5) and \
                    (game.camera.y - 38 < self.rect.y < game.camera.y + SIZE[1] + 5):
                self.Visible = True
                self.draw(game)
            else:
                self.Visible = False

        def draw(self, game):
            if self.move_left:
                self.anim_l.blit(game.screen, game.camera.get_pos(self.rect.x, self.rect.y))
            else:
                self.anim_r.blit(game.screen, game.camera.get_pos(self.rect.x, self.rect.y))

        def collision(self, dx, dy, block, hero):
            collide_objects = [n for n in block if n.Visible and n.Collision] + [hero]
            for n in pygame.Rect.collidelistall(self.rect, collide_objects):
                if collide_objects[n] == hero.rect:
                    hero.hp -= Zombie.damage

                if dx:
                    self.dx = 0
                    if collide_objects[n] in block and self.Ground:
                        self.to_jump = True
                        if collide_objects[n].rect.y < self.rect.y:
                            self.to_jump = False
                    if dx > 0:
                        self.rect.right = collide_objects[n].rect.left
                        self.dx = 0

                    elif dx < 0:
                        self.rect.left = collide_objects[n].rect.right
                        self.dx = 0

                if dy > 0:
                    self.rect.bottom = collide_objects[n].rect.top
                    self.dy = 0
                    if collide_objects[n] in block:
                        self.Ground = True
                        if self.dy > 12:
                            self.hp -= self.dy // 8

                elif dy < 0:
                    self.rect.top = collide_objects[n].rect.bottom
                    self.dy = 0
