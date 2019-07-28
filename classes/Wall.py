if __name__ == 'classes.Wall':

    from data.textures.loader import links
    from settings import SIZE

    import pygame


    class Wall:
        def __init__(self, x, y, name, explored=False):
            self.x, self.y = x, y
            self.name = name
            self.image = links[name]
            self.Visible = False
            self.explored = explored
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y
            self.hp = 10

        def render(self, game):
            if (game.camera.x - 25 < self.x < game.camera.x + SIZE[0]) and \
                    (game.camera.y - 25 < self.y < game.camera.y + SIZE[1]):
                self.Visible = True

                self.draw(game)

                # Трещины
                if self.hp != 10:
                    if 0.7 < self.hp / 10 < 1:
                        img = links['destroy'][0]
                    elif 0.6 < self.hp / 10 <= 0.7:
                        img = links['destroy'][1]
                    elif 0.5 < self.hp / 10 <= 0.6:
                        img = links['destroy'][2]
                    elif 0.4 < self.hp / 10 <= 0.5:
                        img = links['destroy'][3]
                    elif 0.3 < self.hp / 10 <= 0.4:
                        img = links['destroy'][4]
                    elif 0.2 < self.hp / 10 <= 0.3:
                        img = links['destroy'][5]
                    elif 0.1 < self.hp / 10 <= 0.2:
                        img = links['destroy'][6]
                    elif self.hp / 10 <= 0.1:
                        img = links['destroy'][7]
                    game.screen.blit(img, game.camera.get_pos(self.x, self.y))
            else:
                self.Visible = False
                self.hp = 10

        def draw(self, game):
            if self.explored:
                game.screen.blit(self.image, game.camera.get_pos(self.x, self.y))
            else:
                pygame.draw.rect(game.screen, (50, 50, 50), (*game.camera.get_pos(self.x, self.y), 25, 25))
