if __name__ == 'classes.PickUp':

    from data.textures.loader import links
    from settings import SIZE

    import pygame


    class PickUp:
        gravity = 1

        def __init__(self, x, y, name, count=1):
            self.dy = 0
            self.Ground = False
            self.name = name
            self.count = count

            if type(links[name]) == list:
                self.image0 = links[name][0]
            else:
                self.image0 = links[name]
            self.image = pygame.transform.scale(self.image0, (15, 15))

            self.rect = self.image.get_rect()
            self.rect.center = x, y

        def render(self, game):
            if (game.camera.x - 15 < self.rect.x < game.camera.x + SIZE[0]) and (
                    game.camera.y - 15 < self.rect.y < game.camera.y + SIZE[1]):
                # Граитация
                if self.Ground is False:
                    self.dy += PickUp.gravity

                # Перемещение
                self.rect.y += self.dy
                self.collision(self.dy, game.block, game.hero, game.pickup)

                self.draw(game)

        def draw(self, game):
            game.screen.blit(self.image, game.camera.get_pos(self.rect.x, self.rect.y))

        def collision(self, dy, block, hero, pickup):
            self.Ground = False

            collide_objects = [n for n in block if n.Visible and n.Collision]
            for n in pygame.Rect.collidelistall(self.rect, collide_objects):
                if dy > 0:
                    self.rect.bottom = collide_objects[n].rect.top
                    self.dy = 0
                    self.Ground = True
            if pygame.sprite.collide_rect(self, hero):
                if hero.add_item(hero.inventory, [self.name, self.count]):
                    pickup.remove(self)
