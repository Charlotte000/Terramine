if __name__ == 'classes.Block':

    from classes.PickUp import PickUp
    from classes.Wall import Wall

    from data.textures.loader import links, b_wheat
    from settings import SIZE, trees

    from random import randint, choice
    import pygame

    class Block:
        def __init__(self, x, y, name, collision=True, wall=None, content=None, cooldown=None, explored=False):
            self.name = name
            self.Visible = False
            self.explored = explored
            self.glow = False
            self.wall = wall
            self.Collision = collision
            self.cooldown = cooldown
            if content is not None:
                self.content = content
            else:
                self.content = []
    
            if type(links[name]) == list:
                self.resouce = links[name]
                self.image = self.resouce[0]
            else:
                self.image = self.resouce = links[name]
    
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y
    
            if name == 'dirt':
                self.hp = 10
            elif name == 'stone':
                self.hp = 15
            elif name == 'cobblestone':
                self.hp = 15
            elif name == 'wood_planks':
                self.hp = 10
            elif name == 'gold_ore':
                self.hp = 19
            elif name == 'iron_ore':
                self.hp = 18
            elif name == 'diamond_ore':
                self.hp = 23
            elif name == 'grass':
                self.hp = 10
            elif name == 'leaves':
                self.hp = 3
            elif name == 'log':
                self.hp = 10
            elif name == 'bedrock':
                self.hp = 1
            elif name == 'furnace':
                self.hp = 10
                self.Collision = False
            elif name == 'sapling':
                self.Collision = False
                self.hp = 3
                if cooldown is None:
                    self.cooldown = randint(10000, 50000)
            elif name == 'crafting_table':
                self.Collision = False
                self.hp = 10
            elif name == 'ladder':
                self.Collision = False
                self.hp = 5
            elif name == 'door':
                self.hp = 10
                self.rect.width = 6
                self.rect.height = 50
            elif name == 'trapdoor':
                self.hp = 10
                self.rect.height = 6
            elif name == 'chest':
                self.Collision = False
                self.hp = 10
            elif name == 'sand':
                self.hp = 10
            elif name == 'glass':
                self.hp = 3
            elif name == 'torch':
                self.hp = 2
                self.glow = True
                self.Collision = False
            elif name == 'wheat':
                self.hp = 2
                self.Collision = False
                if cooldown is None:
                    self.cooldown = randint(5000, 10000)
            elif name == 'tall_grass':
                self.hp = 2
                self.Collision = False
            elif name == 'altar':
                self.hp = 1
                self.Collision = False
            elif name == 'bed':
                self.hp = 5
                self.Collision = False
            elif name == 'mushroom':
                self.hp = 2
                self.Collision = False
                if cooldown is None:
                    self.cooldown = randint(9000, 18000)
                self.possible_pos = [[x - 25, y], [x - 25, y - 25], [x - 25, y + 25], [x + 25, y], [x + 25, y + 25],
                                     [x + 25, y - 25]]
            elif name == 'wool':
                self.hp = 5
            elif name == 'fence':
                self.hp = 10

            self.hp0 = self.hp
    
        def render(self, game):
            if game.camera.x - self.rect.width < self.rect.x < game.camera.x + SIZE[0] + self.rect.width and\
                    game.camera.y - self.rect.height < self.rect.y < game.camera.y + SIZE[1] + self.rect.height:
                self.Visible = True
    
                self.draw(game)
    
                # Трещины
                if self.hp0 != self.hp:
                    if 0.7 < self.hp0 / self.hp < 1:
                        game.screen.blit(links['destroy'][0], game.camera.get_pos(self.rect.x, self.rect.y))
                    elif 0.6 < self.hp0 / self.hp <= 0.7:
                        game.screen.blit(links['destroy'][1], game.camera.get_pos(self.rect.x, self.rect.y))
                    elif 0.5 < self.hp0 / self.hp <= 0.6:
                        game.screen.blit(links['destroy'][2], game.camera.get_pos(self.rect.x, self.rect.y))
                    elif 0.4 < self.hp0 / self.hp <= 0.5:
                        game.screen.blit(links['destroy'][3], game.camera.get_pos(self.rect.x, self.rect.y))
                    elif 0.3 < self.hp0 / self.hp <= 0.4:
                        game.screen.blit(links['destroy'][4], game.camera.get_pos(self.rect.x, self.rect.y))
                    elif 0.2 < self.hp0 / self.hp <= 0.3:
                        game.screen.blit(links['destroy'][5], game.camera.get_pos(self.rect.x, self.rect.y))
                    elif 0.1 < self.hp0 / self.hp <= 0.2:
                        game.screen.blit(links['destroy'][6], game.camera.get_pos(self.rect.x, self.rect.y))
                    elif self.hp0 / self.hp <= 0.1:
                        game.screen.blit(links['destroy'][7], game.camera.get_pos(self.rect.x, self.rect.y))
            else:
                self.Visible = False
                self.hp0 = self.hp
    
            # Свечение
            if self.glow:
                if (game.camera.x - 100 < self.rect.centerx < game.camera.x + SIZE[0] + 100) and \
                        (game.camera.y - 100 < self.rect.centery < game.camera.y + SIZE[1] + 100):

                    pygame.draw.circle(game.night, (255, 255, 255), game.camera.get_pos(self.rect.centerx,
                                                                                        self.rect.centery, True), 100)
    
            # Рост дерева
            if self.name == 'sapling':
                self.cooldown -= 1
                if self.cooldown <= 0:
                    tree = choice(trees)(self.rect.x, self.rect.y)
    
                    for q in game.block:
                        if q.Visible and (q != self):
                            for w in tree:
                                if (q.rect.x == w[0]) and (q.rect.y == w[1]) and (w[2] == 'leaves'):
                                    tree.remove(w)
                                elif (q.rect.x == w[0]) and (q.rect.y == w[1]) and (w[2] == 'log'):
                                    tree.clear()
                    for q in tree:
                        game.block.append(Block(q[0], q[1], q[2], collision=False, explored=True))
                    game.block.remove(self)
    
            # Рост пшеницы
            if self.name == 'wheat':
                if self.cooldown > 0:
                    self.cooldown -= 1
    
                if self.cooldown >= 2100:
                    self.image = self.resouce[0]
                elif self.cooldown >= 1800:
                    self.image = self.resouce[1]
                elif self.cooldown >= 1500:
                    self.image = self.resouce[2]
                elif self.cooldown >= 1200:
                    self.image = self.resouce[3]
                elif self.cooldown >= 900:
                    self.image = self.resouce[4]
                elif self.cooldown >= 600:
                    self.image = self.resouce[5]
                elif self.cooldown >= 300:
                    self.image = self.resouce[6]
                elif self.cooldown >= -1:
                    self.image = self.resouce[7]
    
            # Рост грибов
            if self.name == 'mushroom':
                if self.cooldown > 0:
                    self.cooldown -= 1
                if self.cooldown == 0:
                    self.cooldown = -1
    
                    for q in game.block:
                        for pos in self.possible_pos:
                            if (q.rect.x == pos[0]) and (q.rect.y == pos[1]):
                                self.possible_pos.remove(pos)
    
                    for pos in range(len(self.possible_pos) - 1, -1, -1):
                        for q in game.block:
                            if q.Collision and (q.rect.x == self.possible_pos[pos][0]) and \
                                    (q.rect.y == self.possible_pos[pos][1] + 25):
                                break
                        else:
                            self.possible_pos.remove(self.possible_pos[pos])
    
                    if self.possible_pos:
                        choice_pos = choice(self.possible_pos)
                        game.block.append(Block(choice_pos[0], choice_pos[1], 'mushroom', explored=True))
                        del choice_pos
    
            # Двери & люки & заборы
            if (self.name == 'door') or (self.name == 'trapdoor') or (self.name == 'fence'):
                if self.Collision:
                    self.image = self.resouce[1]
                else:
                    self.image = self.resouce[0]

        def destroy(self, game):
            if self.name == 'grass':
                game.pickup.append(PickUp(self.rect.centerx, self.rect.centery, 'dirt'))
            elif self.name == 'stone':
                game.pickup.append(PickUp(self.rect.centerx, self.rect.centery, 'cobblestone'))
            elif self.name == 'leaves':
                if randint(0, 2) == 1:
                    game.pickup.append(PickUp(self.rect.centerx, self.rect.centery, 'sapling'))
            elif self.name == 'diamond_ore':
                game.pickup.append(PickUp(self.rect.centerx, self.rect.centery, 'diamond'))
            elif self.name == 'door':
                game.pickup.append(PickUp(self.rect.centerx, self.rect.centery, 'door'))
            elif self.name == 'trapdoor':
                game.pickup.append(PickUp(self.rect.centerx, self.rect.centery, 'trapdoor'))
            elif self.name == 'wheat':
                game.pickup.append(PickUp(self.rect.centerx, self.rect.centery, 'wheat_seed'))
                if self.image == b_wheat[7]:
                    for count in range(0, randint(0, 2)):
                        game.pickup.append(PickUp(self.rect.centerx, self.rect.centery, 'wheat_seed'))
                    for count in range(0, randint(1, 4)):
                        game.pickup.append(
                            PickUp(self.rect.centerx, self.rect.centery, 'grown_wheat'))
            elif self.name == 'tall_grass':
                if 1 == randint(1, 5):
                    game.pickup.append(PickUp(self.rect.centerx, self.rect.centery, 'wheat_seed'))
            elif self.name == 'bed':
                game.pickup.append(PickUp(self.rect.centerx, self.rect.centery, self.name))
                for point in game.hero.spawn_point:
                    if point == [self.rect.x, self.rect.y - 25]:
                        game.hero.spawn_point.remove(point)
            elif self.name != 'glass':
                game.pickup.append(PickUp(self.rect.centerx, self.rect.centery, self.name))

            if self.wall:
                game.wall.append(Wall(self.rect.x, self.rect.y, self.wall, explored=True))

            for b in game.block + game.wall:
                if b.Visible:
                    if [b.rect.x, b.rect.y] in [[self.rect.x, self.rect.y - 25], [self.rect.x, self.rect.y + 25],
                                                      [self.rect.x - 25, self.rect.y], [self.rect.x + 25, self.rect.y]]:
                        b.explored = True
            game.block.remove(self)

        def draw(self, game):
            if self.explored:
                game.screen.blit(self.image, game.camera.get_pos(self.rect.x, self.rect.y))
            else:
                pygame.draw.rect(game.screen, (50, 50, 50), (*game.camera.get_pos(self.rect.x, self.rect.y),
                                                             self.rect.width, self.rect.height))
