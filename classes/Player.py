if __name__ == 'classes.Player':
    from settings import F_SIZE, axe_damage, pickaxe_damage, shovel_damage

    from classes.Block import Block
    from classes.Wall import Wall
    from classes.Sheep import Sheep
    from classes.Arrow import Arrow
    from classes.Eye import Eye
    from classes.EyeServant import EyeServant
    from classes.Cthulhu import Cthulhu
    from classes.Worm import Worm

    import pygame
    from pyganim import PygAnimation
    from math import sqrt

    class Player:
        gravity = 1

        def __init__(self, player_x, player_y):
            # -Настройки-
            self.Move = 0.5
            self.Max_Speed = 2.5
            self.Jump = 8
            self.reach = 75
            self.block_damage = 1
            self.damage = 0.2
            self.hp = self.hp0 = 10
            self.hunger = 10
            self.inventory = []
            self.cooldown = self.cooldown0 = 8
            self.bow_cooldown = self.bow_cooldown0 = 16
            self.spawn_point = []
            # -----------
            self.x, self.y = player_x, player_y
            self.dx = self.dy = 0
            self.Ground = False
            self.ladder = False
            self.left = self.right = self.up = self.down = self.left_click = self.right_click = \
                self.k_up = self.k_down = self.k_left = self.k_right = self.q = False
            self.anim_l = False
            self.cursor = [0, 0]
            self.hp_img = pygame.image.load(r'data\textures\icons.png').convert_alpha().subsurface(9, 0, 9, 9)
            self.hunger_img = pygame.image.load(r'data\textures\icons.png').convert_alpha().subsurface(18, 0, 9, 9)
            self.armor_img = pygame.image.load(r'data\textures\icons.png').convert_alpha().subsurface(0, 0, 9, 9)

            self.craft_available = []
            self.furnace_available = []

            self.inventory_menu_pos = 1
            self.menu_pos = 1

            self.chest_block = None

            resource = pygame.image.load(r'data\textures\player.png').convert_alpha()
            self.rect = pygame.Rect(player_x, player_y, 22, 49)

            self.walk_r = PygAnimation([[resource.subsurface((count * 22, 0, 22, 49)), 100] for count in range(0, 7)])
            self.walk_r.play()

            self.walk_l = PygAnimation([[resource.subsurface((count * 22, 49, 22, 49)), 100] for count in range(0, 7)])
            self.walk_l.play()

            self.stay_r = PygAnimation([[resource.subsurface((0, 98, 22, 49)), 100]])
            self.stay_r.play()

            self.stay_l = PygAnimation([[resource.subsurface((22, 98, 22, 49)), 100]])
            self.stay_l.play()

        def render(self, game):
            # Обработка нажатий клавиш
            self.key_event(game)

            # Счётчики
            if self.cooldown < self.cooldown0:
                self.cooldown -= 1
            if self.cooldown <= 0:
                self.cooldown = self.cooldown0
            if self.bow_cooldown0 < self.bow_cooldown:
                self.bow_cooldown0 -= 1
            if self.bow_cooldown0 <= 0:
                self.bow_cooldown0 = self.bow_cooldown

            # Мышь
            self.cursor = pygame.mouse.get_pos()

            # Количество жизней, голод и броня
            if self.hp0 > 10:
                if (0 < self.hp <= self.hp0 - 0.015) and (self.hunger - 0.005 > 0):
                    self.hp += 0.015
                    self.hunger -= 0.005
            else:
                if (0 < self.hp <= self.hp0 - 0.005) and (self.hunger - 0.005 > 0):
                    self.hp += 0.005
                    self.hunger -= 0.005
            if self.hunger > 10:
                self.hunger = 10
            elif self.hunger > 0:
                self.hunger -= 0.0005
            else:
                self.hp -= 0.001

            _hp = 0
            for item in self.inventory:
                if item[0] == 'iron_helmet':
                    _hp += 3
                elif item[0] == 'iron_chestplate':
                    _hp += 3
                elif item[0] == 'iron_leggings':
                    _hp += 2
                elif item[0] == 'iron_boots':
                    _hp += 2
            self.hp0 = 10 + _hp
            if self.hp > self.hp0:
                self.hp = self.hp0
            del _hp

            # Лестница
            if self.ladder:
                self.dy = 0
                if self.up:
                    self.dy -= self.Jump - 1
                if self.down:
                    self.dy += self.Max_Speed
                if (self.up is False) and (self.down is False):
                    if self.dy + self.Move < 0:
                        self.dy += self.Move
                    elif self.dy - self.Move > 0:
                        self.dy -= self.Move
                    else:
                        self.dy = 0

            # Границы мира
            if (self.x <= 0) and (self.dx < 0):
                self.dx = 0
            if (self.x + 22 >= F_SIZE[0]) and (self.dx > 0):
                self.dx = 0
            if (self.y + 49 >= F_SIZE[1]) and (self.dy > 0):
                self.dy = 0

            # Гравитация
            if (self.Ground is False) and (self.ladder is False):
                self.dy += Player.gravity
            self.Ground = False
            self.ladder = False

            # Торможение
            if (self.left is False) and (self.right is False):
                if self.dx + self.Move < 0:
                    self.dx += self.Move
                elif self.dx - self.Move > 0:
                    self.dx -= self.Move
                else:
                    self.dx = 0
            if self.dx > self.Max_Speed:
                self.dx -= self.Move
            elif self.dx < -self.Max_Speed:
                self.dx += self.Move

            self.draw(game)

            # Перемещение
            self.x += self.dx
            self.y += self.dy

            # Столкновение
            self.rect.x = self.x
            self.collision(self.dx, 0, game.block, game.wall, game.enemy)

            self.rect.y = self.y
            self.collision(0, self.dy, game.block, game.wall, game.enemy)

        def collision(self, dx, dy, block, wall, enemy):
            collide_objects = [n for n in block if n.Visible and
                               (n.Collision or n.name == 'ladder' or n.name == 'chest')] + \
                              [en for en in enemy if type(en) not in [Eye, EyeServant, Cthulhu, Worm]] + \
                              [w for w in wall if not w.explored]
            for n in pygame.Rect.collidelistall(self.rect, collide_objects):
                if (collide_objects[n] in block) and (collide_objects[n].name == 'ladder'):
                    self.ladder = True
                else:
                    collide_objects[n].explored = True

                    if collide_objects[n] in block and collide_objects[n].name == 'chest':
                        continue
                    if collide_objects[n] in wall:
                        continue
                    if dx > 0:
                        self.rect.right = collide_objects[n].rect.left
                        self.dx = 0
                        self.x = self.rect.x
                    elif dx < 0:
                        self.rect.left = collide_objects[n].rect.right
                        self.dx = 0
                        self.x = self.rect.x
                    if dy > 0:
                        self.rect.bottom = collide_objects[n].rect.top
                        self.y = self.rect.y
                        if self.dy > 12:
                            self.hp -= self.dy // 3
                        self.Ground = True
                        self.dy = 0
                    elif dy < 0:
                        self.rect.top = collide_objects[n].rect.bottom
                        self.dy = 0
                        self.y = self.rect.y

        def draw(self, game):
            # Отображение
            if self.dx > 0:
                self.walk_r.blit(game.screen, game.camera.get_pos(self.x, self.y))
                self.anim_l = False
            elif self.dx < 0:
                self.walk_l.blit(game.screen, game.camera.get_pos(self.x, self.y))
                self.anim_l = True
            elif self.anim_l:
                self.stay_l.blit(game.screen, game.camera.get_pos(self.x, self.y))
            else:
                self.stay_r.blit(game.screen, game.camera.get_pos(self.x, self.y))

        def key_event(self, game):
            if self.left:
                if self.dx - self.Move >= -self.Max_Speed:
                    self.dx -= self.Move

            if self.right:
                if self.dx + self.Move <= self.Max_Speed:
                    self.dx += self.Move

            if self.up:
                if self.Ground and self.ladder is False:
                    self.dy -= self.Jump

            if self.left_click:
                xx, yy = game.camera.get_pos(self.rect.centerx, self.rect.centery)
                if sqrt(pow(self.cursor[0] - xx, 2) + pow(self.cursor[1] - yy, 2)) <= self.reach and \
                   ((self.inventory_menu_pos <= len(self.inventory) and self.inventory[self.inventory_menu_pos - 1][0] != 'bow') or \
                    self.inventory_menu_pos > len(self.inventory)):
                    for e in game.enemy:
                        _x, _y = game.camera.get_pos(e.rect.x, e.rect.y)
                        if (_x < self.cursor[0] < _x + e.rect.width) and (_y < self.cursor[1] < _y + e.rect.height):
                            _dx = 8
                            e.hp -= self.damage
                            if self.inventory_menu_pos <= len(self.inventory):
                                if self.inventory[self.inventory_menu_pos - 1][0] == 'wooden_sword':
                                    e.hp -= 0.4
                                    _dx += 2
                                elif self.inventory[self.inventory_menu_pos - 1][0] == 'stone_sword':
                                    e.hp -= 0.8
                                    _dx += 4
                                elif self.inventory[self.inventory_menu_pos - 1][0] == 'iron_sword':
                                    e.hp -= 1.2
                                    _dx += 6
                                elif self.inventory[self.inventory_menu_pos - 1][0] == 'golden_sword':
                                    e.hp -= 1.6
                                    _dx += 8
                                elif self.inventory[self.inventory_menu_pos - 1][0] == 'diamond_sword':
                                    e.hp -= 2
                                    _dx += 10
                            if type(e) not in [Eye, EyeServant, Cthulhu, Worm]:
                                if self.x < e.rect.x:
                                    e.dx += _dx
                                else:
                                    e.dx -= _dx
                                e.dy -= 5
                            del _dx
                            break
                        del _x, _y
                    else:
                        for a in game.animals['pig'] + game.animals['sheep']:
                            _x, _y = game.camera.get_pos(a.rect.x, a.rect.y)
                            if (_x < self.cursor[0] < _x + a.rect.width) and (_y < self.cursor[1] < _y + a.rect.height):

                                if (a in game.animals['sheep']) and (self.inventory_menu_pos <= len(self.inventory)) and \
                                        (self.inventory[self.inventory_menu_pos - 1][0] == 'scissors'):
                                    if a.grow_time0 == Sheep.grow_time:
                                        a.grow_time0 -= 1
                                    break

                                _dx = 8
                                a.hp -= self.damage
                                if self.inventory_menu_pos <= len(self.inventory):
                                    if self.inventory[self.inventory_menu_pos - 1][0] == 'wooden_sword':
                                        a.hp -= self.damage * 2
                                        _dx += 2
                                    elif self.inventory[self.inventory_menu_pos - 1][0] == 'stone_sword':
                                        a.hp -= self.damage * 4
                                        _dx += 4
                                    elif self.inventory[self.inventory_menu_pos - 1][0] == 'iron_sword':
                                        a.hp -= self.damage * 6
                                        _dx += 6
                                    elif self.inventory[self.inventory_menu_pos - 1][0] == 'golden_sword':
                                        a.hp -= self.damage * 8
                                        _dx += 8
                                    elif self.inventory[self.inventory_menu_pos - 1][0] == 'diamond_sword':
                                        a.hp -= self.damage * 10
                                        _dx += 10
                                if self.x < a.rect.x:
                                    a.dx += _dx
                                else:
                                    a.dx -= _dx
                                a.dy -= 5
                                del _dx
                                break
                            del _x, _y
                        else:
                            for n in game.block:
                                if n.Visible and n.explored:
                                    _x, _y = game.camera.get_pos(n.rect.x, n.rect.y)
                                    if (_x + 1 <= self.cursor[0] <= _x + 24) and (_y + 1 <= self.cursor[1] <= _y + 24):
                                        if (n.name != 'bedrock') and (n.name != 'altar'):
                                            n.hp0 -= self.block_damage
                                            if self.inventory_menu_pos <= len(self.inventory):
                                                _name = self.inventory[self.inventory_menu_pos - 1][0]
                                                if n.name in axe_damage:
                                                    if _name == 'wooden_axe':
                                                        n.hp0 -= self.block_damage * 0.7
                                                    elif _name == 'stone_axe':
                                                        n.hp0 -= self.block_damage * 1.1
                                                    elif _name == 'iron_axe':
                                                        n.hp0 -= self.block_damage * 1.5
                                                    elif _name == 'golden_axe':
                                                        n.hp0 -= self.block_damage * 1.9
                                                    elif _name == 'diamond_axe':
                                                        n.hp0 -= self.block_damage * 2.3
                                                if n.name in pickaxe_damage:
                                                    if _name == 'wooden_pickaxe':
                                                        n.hp0 -= self.block_damage * 0.7
                                                    elif _name == 'stone_pickaxe':
                                                        n.hp0 -= self.block_damage * 1.4
                                                    elif _name == 'iron_pickaxe':
                                                        n.hp0 -= self.block_damage * 2.1
                                                    elif _name == 'golden_pickaxe':
                                                        n.hp0 -= self.block_damage * 2.8
                                                    elif _name == 'diamond_pickaxe':
                                                        n.hp0 -= self.block_damage * 3.5
                                                if n.name in shovel_damage:
                                                    if _name == 'wooden_shovel':
                                                        n.hp0 -= self.block_damage * 0.7
                                                    elif _name == 'stone_shovel':
                                                        n.hp0 -= self.block_damage * 1.4
                                                    elif _name == 'iron_shovel':
                                                        n.hp0 -= self.block_damage * 2.1
                                                    elif _name == 'golden_shovel':
                                                        n.hp0 -= self.block_damage * 2.8
                                                    elif _name == 'diamond_shovel':
                                                        n.hp0 -= self.block_damage * 3.5
                                        break
                                    del _x, _y
                            else:
                                for n in game.wall:
                                    if n.Visible:
                                        _x, _y = game.camera.get_pos(n.x, n.y)
                                        if (_x + 1 <= self.cursor[0] <= _x + 24) and (_y + 1 <= self.cursor[1] <= _y + 24):
                                            if self.inventory_menu_pos <= len(self.inventory):
                                                if self.inventory[self.inventory_menu_pos - 1][0] == 'wooden_hammer':
                                                    n.hp -= self.block_damage * 1.7
                                                elif self.inventory[self.inventory_menu_pos - 1][0] == 'stone_hammer':
                                                    n.hp -= self.block_damage * 2.4
                                                elif self.inventory[self.inventory_menu_pos - 1][0] == 'iron_hammer':
                                                    n.hp -= self.block_damage * 3.1
                                                elif self.inventory[self.inventory_menu_pos - 1][0] == 'golden_hammer':
                                                    n.hp -= self.block_damage * 3.8
                                                elif self.inventory[self.inventory_menu_pos - 1][0] == 'diamond_hammer':
                                                    n.hp -= self.block_damage * 4.5
                                                if n.hp <= 0:
                                                    game.wall.remove(n)
                                            break

                if self.inventory_menu_pos <= len(self.inventory):
                    if self.inventory[self.inventory_menu_pos - 1][0] == 'bow' and \
                            self.bow_cooldown0 == self.bow_cooldown:
                        self.bow_cooldown0 -= 1
                        for item in self.inventory:
                            if item[0] == 'arrow':
                                item[1] -= 1
                                game.arrow.append(Arrow(self.rect.centerx, self.rect.centery,
                                                        self.cursor[0] + game.camera.x, self.cursor[1] + game.camera.y))
                                break

            if self.right_click:
                xx, yy = game.camera.get_pos(self.rect.centerx, self.rect.centery)
                if sqrt(pow(self.cursor[0] - xx, 2) + pow(self.cursor[1] - yy, 2)) <= self.reach:
                    go = True
                    _x = round((self.cursor[0] + game.camera.x - 12) / 25) * 25
                    _y = round((self.cursor[1] + game.camera.y - 12) / 25) * 25

                    if (self.x - 25 < _x < self.x + 21) and (self.y - 25 < _y < self.y + 49):
                        go = False

                    _name = ''

                    if self.inventory_menu_pos <= len(self.inventory):
                        if self.inventory[self.inventory_menu_pos - 1][1] <= 0:
                            go = False
                        else:
                            _name = self.inventory[self.inventory_menu_pos - 1][0]
                    else:
                        go = False

                    if _name == 'bread':
                        self.inventory[self.inventory_menu_pos - 1][1] -= 1
                        go = False
                        self.hunger += 2
                    if _name == 'mushroom_stew':
                        self.inventory[self.inventory_menu_pos - 1][1] -= 1
                        go = False
                        self.hunger += 3
                    if _name in ['cooked_porkchop', 'cooked_fowl', 'cooked_mutton']:
                        self.inventory[self.inventory_menu_pos - 1][1] -= 1
                        go = False
                        self.hunger += 4

                    if _name[-3:] == 'axe' or _name[-7:] == 'pickaxe' or _name[-6:] == 'shovel' or \
                            _name[-5:] == 'sword' or _name[-6:] == 'hammer' or _name == 'grown_wheat' or \
                            _name[-8:] == 'porkchop' or _name == 'arrow' or _name == 'bow' or  _name[-4:] == 'fowl' or \
                            _name[-5:] == 'ingot' or _name == 'diamond' or _name == 'iron_helmet' or \
                            _name == 'iron_chestplate' or _name == 'iron_leggings' or _name == 'iron_boots' or \
                            _name == 'eye_call' or _name[-6:] == 'mutton' or _name == 'thread' or _name == 'stick' or \
                            _name == 'scissors' or _name == 'coal':
                        go = False

                    for n in game.block:
                        if n.Visible:
                            if (n.name == 'door') and (n.rect.x == _x) and (_y - 25 <= n.rect.y <= _y):
                                go = False
                                if n.Collision:
                                    n.Collision = False
                                elif n.Collision is False:
                                    if pygame.sprite.collide_rect(self, n) == 0:
                                        n.Collision = True
                            if (n.name == 'bed') and (_x - 25 <= n.rect.x <= _x) and (n.rect.y == _y):
                                go = False

                            if ((n.name == 'trapdoor') or (n.name == 'fence')) and (n.rect.x == _x) and (_y == n.rect.y):
                                go = False
                                if n.Collision:
                                    n.Collision = False
                                elif n.Collision is False:
                                    if pygame.sprite.collide_rect(self, n) == 0:
                                        n.Collision = True

                            if (n.rect.x == _x) and (n.rect.y == _y):
                                go = False

                                if (n.name == 'altar') and (_name == 'eye_call'):
                                    for qwe in self.inventory:
                                        if qwe[0] == 'eye_call':
                                            qwe[1] -= 1
                                    game.enemy.append(Eye(self.x - 800, self.y - 800))
                                    go = False

                                if n.name == 'chest':
                                    if self.chest_block is None:
                                        self.chest_block = n
                                    else:
                                        self.chest_block = None

                            if (_name == 'door') and (n.rect.x == _x) and (_y <= n.rect.y <= _y + 49):
                                go = False
                            if (_name == 'bed') and (n.rect.x == _x + 25) and (n.rect.y == _y):
                                go = False

                    if _name[-4:] == 'wall':
                        for n in game.wall:
                            if n.Visible:
                                if (n.x == _x) and (n.y == _y):
                                    go = False
                                    break

                    for e in game.enemy:
                        if (e.rect.x - 25 < _x < e.rect.x + 3) and (e.rect.y - 25 < _y < e.rect.y + 63):
                            go = False

                    if (_name == 'sapling') or (_name == 'wheat_seed'):
                        for q in game.block:
                            if q.Visible:
                                if (_x == q.rect.x) and (_y + 25 == q.rect.y) and (
                                        (q.name == 'dirt') or (q.name == 'grass')):
                                    break
                        else:
                            go = False
                    if _name == 'wheat_seed':
                        for q in game.animals['sheep'] + game.animals['pig']:
                            q_x, q_y = game.camera.get_pos(q.rect.x, q.rect.y)
                            if q_x < self.cursor[0] < q_x + q.rect.width and \
                                    q_y < self.cursor[1] < q_y + q.rect.height and q.active_cooldown == 0 and \
                                    q.active == type(q).active_time:
                                go = False
                                q.active = 0
                                self.inventory[self.inventory_menu_pos - 1][1] -= 1
                                break

                    if _name == 'mushroom':
                        for q in game.block:
                            if q.Visible and q.Collision:
                                if (_x == q.rect.x) and (_y + 25 == q.rect.y):
                                    break
                        else:
                            go = False

                    if go:
                        if _name == 'bed':
                            self.spawn_point.append([_x, _y - 25])
                        if _name[-4:] == 'wall':
                            self.inventory[self.inventory_menu_pos - 1][1] -= 1
                            game.wall.append(Wall(_x, _y, self.inventory[self.inventory_menu_pos - 1][0], explored=True))
                        else:
                            self.inventory[self.inventory_menu_pos - 1][1] -= 1
                            if self.inventory[self.inventory_menu_pos - 1][0] != 'wheat_seed':
                                game.block.append(Block(_x, _y, self.inventory[self.inventory_menu_pos - 1][0],
                                                        explored=True))
                            else:
                                game.block.append(Block(_x, _y, 'wheat', explored=True))

                    del _x, _y, _name, go

            if self.k_up:
                if self.chest_block:
                    if self.menu_pos <= len(self.chest_block.content):
                        if self.add_item(self.inventory, [self.chest_block.content[self.menu_pos - 1][0], 1]):
                            self.remove_item(self.chest_block.content, [self.chest_block.content[self.menu_pos - 1][0], 1])
                elif self.furnace_available:
                    if self.menu_pos <= len(self.furnace_available):
                        if self.add_item(self.inventory, self.furnace_available[self.menu_pos - 1][0]):
                            for rem_item in self.furnace_available[self.menu_pos - 1][1]:
                                self.remove_item(self.inventory, rem_item)
                else:
                    if self.menu_pos <= len(self.craft_available):
                        if self.add_item(self.inventory, self.craft_available[self.menu_pos - 1][0]):
                            for rem_item in self.craft_available[self.menu_pos - 1][1]:
                                self.remove_item(self.inventory, rem_item)

                self.k_up = False

            if self.k_down:
                if self.chest_block:
                    if self.inventory_menu_pos <= len(self.inventory):
                        if self.add_item(self.chest_block.content, [self.inventory[self.inventory_menu_pos - 1][0], 1]):
                            self.remove_item(self.inventory, [self.inventory[self.inventory_menu_pos - 1][0], 1])

                self.k_down = False

            if self.k_left:
                self.menu_pos -= 1
                self.k_left = False

            if self.k_right:
                self.menu_pos += 1
                self.k_right = False

            if self.q:
                if self.inventory_menu_pos <= len(self.inventory):
                    if pygame.key.get_mods() == 1:
                        self.inventory[self.inventory_menu_pos - 1][1] -= 50
                    else:
                        self.inventory[self.inventory_menu_pos - 1][1] -= 1
                self.q = False

        def add_item(self, inventory, item):
            for z in inventory:
                if z[0] == item[0]:
                    z[1] += item[1]
                    return True
            if len(inventory) < 19:
                inventory.append(item[:])
                return True
            return False

        def remove_item(self, inventory, item):
            for i in inventory:
                if i[0] == item[0]:
                    if i[1] > item[1]:
                        i[1] -= item[1]
                        return True
                    elif i[1] == item[1]:
                        inventory.remove(i)
                        return True
            return False
