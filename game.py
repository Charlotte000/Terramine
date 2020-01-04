from random import randint
from math import sqrt, ceil
from datetime import datetime
from os import listdir, remove
import pygame

from classes.Arrow import Arrow
from classes.Bird import Bird
from classes.Block import Block
from classes.Camera import Camera
from classes.Cthulhu import Cthulhu
from classes.Eye import Eye
from classes.EyeServant import EyeServant
from classes.PickUp import PickUp
from classes.Pig import Pig
from classes.Player import Player
from classes.Sheep import Sheep
from classes.Wall import Wall
from classes.Worm import Worm
from classes.Zombie import Zombie
from classes.Button import Button

from data.textures.loader import t_iron_pickaxe, links
from settings import SIZE, F_SIZE, DEBUG, description, craft_list, crafting_table_list, minimap, furnace_list, keyBindings
from utils import read_save, write_save, create_map

pygame.font.init()
font = pygame.font.Font(r'data\font.ttf', 10)


class Game:
    def __init__(self):
        self.game = True

        self.save_name = self.main_menu()

        # Game Objects
        self.hero = Player(4500, 500)
        self.pickup = []
        self.enemy = []
        self.animals = {'pig': [], 'bird': [], 'sheep': []}
        self.wall = []
        self.arrow = []
        self.camera = Camera()
        self.block = []

        # Game Screens
        self.screen = pygame.Surface(SIZE)
        self.menu = pygame.Surface((SIZE[0], 56))
        self.night = pygame.Surface(SIZE)
        self.hp_menu = pygame.Surface((95, 25))

        self.night.set_colorkey((255, 255, 255))
        self.time = [0]
        self.time_speed = [0.01]
        self.night.set_alpha(self.time[0])

        # Reading save
        if self.save_name:
            read_save(self.save_name, self.hero, self.block, self.wall, self.animals, self.time, self.time_speed)
        else:
            # Creating new map
            create_map(self.hero, self.block, self.wall, window)
        self.time = self.time[0]
        self.time_speed = self.time_speed[0]

    def loop(self):
        inventory_cells = [pygame.Rect(SIZE[0] / 2 + (i - 5) * 26 + 1, SIZE[1] + 1, 26, 26) for i in range(10)]
        menu_cells = [pygame.Rect(i * 26 + 1, SIZE[1] + 1 + 26, 26, 26) for i in range(24)]

        while self.game:
            time0 = datetime.now()

            # Заливка экрана
            self.screen.fill((14, 166, 241))
            self.night.fill((0, 0, 0))

            # Звёзды
            if (self.time > 120) and (self.hero.hp > 0):
                if self.time_speed > 0:
                    self.time += 0.02
                else:
                    self.time -= 0.02
                pygame.draw.circle(self.screen, (255, 255, 255), (440, 405), 2)
                pygame.draw.circle(self.screen, (255, 255, 255), (85, 133), 2)
                pygame.draw.circle(self.screen, (255, 255, 255), (31, 397), 2)
                pygame.draw.circle(self.screen, (255, 255, 255), (353, 156), 2)
                pygame.draw.circle(self.screen, (255, 255, 255), (376, 402), 2)
                pygame.draw.circle(self.screen, (255, 255, 255), (286, 275), 2)
                pygame.draw.circle(self.screen, (255, 255, 255), (175, 252), 2)
                pygame.draw.circle(self.screen, (255, 255, 255), (15, 456), 2)
                pygame.draw.circle(self.screen, (255, 255, 255), (391, 443), 2)
                pygame.draw.circle(self.screen, (255, 255, 255), (32, 278), 2)
                pygame.draw.circle(self.screen, (255, 255, 255), (178, 134), 2)

            # Key event
            self.key_read()

            # Рендер
            self.game_objects_render()

            # Жизни босса
            for e in self.enemy:
                if type(e) in [Cthulhu, Eye]:
                    name = e.__class__.__name__
                    pygame.draw.rect(self.screen, (107, 105, 105), (SIZE[0] / 2 - 100, 10, 200, 30))
                    pygame.draw.rect(self.screen, (215, 215, 215), (SIZE[0] / 2 - 100, 10, 200, 30), 1)
                    self.screen.blit(font.render(name, True, (255, 255, 255)),
                                     (SIZE[0] / 2 - font.size(name)[0] / 2, 15))
                    w = e.hp / type(e).hp * 160
                    pygame.draw.rect(self.screen, (255, 50, 50), (SIZE[0] / 2 - w / 2, 30, w, 3))

            # Добавление мобов
            if self.time > 120:
                if len(self.enemy) < 4:
                    if 1 == randint(1, 50):
                        self.add_zombie()
            if len(self.animals['pig']) < 2:
                self.add_pig()
            if len(self.animals['bird']) < 1:
                self.add_bird()
            if len(self.animals['sheep']) < 2:
                self.add_sheep()

            # Меню инвентаря
            self.menu.fill((107, 105, 105))
            pygame.draw.rect(self.menu, (215, 215, 215), (0, 0, SIZE[0], 28), 1)
            self.menu.blit(font.render('Inventory', True, (255, 255, 255)), (SIZE[0] - 61, 1))

            # Cursor borders
            if self.hero.inventory_menu_pos <= 0:
                self.hero.inventory_menu_pos = 1
            elif self.hero.inventory_menu_pos > len(inventory_cells):
                self.hero.inventory_menu_pos = len(inventory_cells)

            for index, cell in enumerate(inventory_cells):
                if self.hero.inventory[index]:
                    # Draw image
                    if isinstance(links[self.hero.inventory[index][0]], list):
                        self.menu.blit(pygame.transform.scale(links[self.hero.inventory[index][0]][0], (20, 20)),
                                       (3 + cell.x, 3 + cell.y - SIZE[1]))
                    else:
                        self.menu.blit(pygame.transform.scale(links[self.hero.inventory[index][0]], (20, 20)),
                                       (3 + cell.x, 3 + cell.y - SIZE[1]))

                    # Draw item count
                    if self.hero.inventory[index][0] in ['sand', 'diamond', 'glass', 'wool']:
                        self.menu.blit(font.render(str(self.hero.inventory[index][1]), False, (0, 0, 0)),
                                       (3 + cell.x, 3 + cell.y - SIZE[1]))
                    else:
                        self.menu.blit(font.render(str(self.hero.inventory[index][1]), False, (212, 212, 212)),
                                       (3 + cell.x, 3 + cell.y - SIZE[1]))

                    # Delete item
                    if self.hero.inventory[index][1] <= 0:
                        self.hero.inventory[index] = None

                # Draw outline
                if index + 1 == self.hero.inventory_menu_pos:
                    pygame.draw.rect(self.menu, (255, 255, 255), (cell.x, cell.y - SIZE[1], cell.w, cell.h), 1)

            # Меню печи
            self.hero.furnace_available.clear()
            for n in self.block:
                if n.Visible and (n.name == 'furnace'):
                    if sqrt(pow(self.hero.rect.centerx - n.rect.centerx, 2) +
                            pow(self.hero.rect.centery - n.rect.centery, 2)) < 45:
                        for ct in furnace_list:
                            for n0 in ct[1]:
                                for item in [i for i in self.hero.inventory if i]:
                                    if (n0[0] == item[0]) and (n0[1] <= item[1]):
                                        break
                                else:
                                    break
                            else:
                                self.hero.furnace_available.append(ct)
                        break
            if self.hero.furnace_available:
                if self.hero.menu_pos > len(self.hero.furnace_available):
                    self.hero.menu_pos = len(self.hero.furnace_available)
                if (self.hero.menu_pos == 0) and (len(self.hero.furnace_available) > 0):
                    self.hero.menu_pos = 1

                pygame.draw.rect(self.menu, (215, 215, 215), (0, 28, SIZE[0], 28), 1)
                self.menu.blit(font.render('Furnace', True, (255, 255, 255)), (SIZE[0] - 51, 29))

                for index, cell in enumerate(menu_cells[:len(self.hero.furnace_available)],
                                             start=max(0, self.hero.menu_pos - len(menu_cells))):
                    # Draw image
                    if isinstance(links[self.hero.furnace_available[index][0][0]], list):
                        self.menu.blit(pygame.transform.scale(links[self.hero.furnace_available[index][0][0]][0],
                                                              (20, 20)), (3 + cell.x, 3 + cell.y - SIZE[1]))
                    else:
                        self.menu.blit(pygame.transform.scale(links[self.hero.furnace_available[index][0][0]],
                                                              (20, 20)), (3 + cell.x, 3 + cell.y - SIZE[1]))

                    # Draw item count
                    self.menu.blit(font.render(str(self.hero.furnace_available[index][0][1]), False, (255, 255, 255)),
                                   (3 + cell.x, 3 + cell.y - SIZE[1]))

                    # Draw outline
                    if index + 1 == self.hero.menu_pos:
                        pygame.draw.rect(self.menu, (255, 255, 255),
                                         (cell.x, cell.y - SIZE[1], cell.w, cell.h), 1)

            else:
                # Меню крафта
                pygame.draw.rect(self.menu, (215, 215, 215), (0, 28, SIZE[0], 28), 1)
                self.menu.blit(font.render('Craft', True, (255, 255, 255)), (SIZE[0] - 35, 29))

                # Adding item in craft list
                self.hero.craft_available.clear()
                for n in craft_list:
                    for n0 in n[1]:
                        for item in [i for i in self.hero.inventory if i]:
                            if (n0[0] == item[0]) and (n0[1] <= item[1]):
                                break
                        else:
                            break
                    else:
                        self.hero.craft_available.append(n)

                for n in self.block:
                    if n.Visible and (n.name == 'crafting_table'):
                        if sqrt(pow(self.hero.x - n.rect.x - 1, 2) + pow(self.hero.y - n.rect.y + 12, 2)) < 45:
                            for ct in crafting_table_list:
                                for n0 in ct[1]:
                                    for item in [i for i in self.hero.inventory if i]:
                                        if (n0[0] == item[0]) and (n0[1] <= item[1]):
                                            break
                                    else:
                                        break
                                else:
                                    self.hero.craft_available.append(ct)
                            break

                # Cursor borders
                if self.hero.menu_pos > len(self.hero.craft_available):
                    self.hero.menu_pos = len(self.hero.craft_available)
                if (self.hero.menu_pos == 0) and (len(self.hero.craft_available) > 0):
                    self.hero.menu_pos = 1

                for index, cell in enumerate(menu_cells[:min(len(self.hero.craft_available), len(menu_cells))],
                                             start=max(0, self.hero.menu_pos - len(menu_cells))):
                    # Draw image
                    if isinstance(links[self.hero.craft_available[index][0][0]], list):
                        self.menu.blit(pygame.transform.scale(links[self.hero.craft_available[index][0][0]][0],
                                                              (20, 20)), (3 + cell.x, 5 + cell.y - SIZE[1]))
                    else:
                        self.menu.blit(pygame.transform.scale(links[self.hero.craft_available[index][0][0]],
                                                              (20, 20)), (3 + cell.x, 5 + cell.y - SIZE[1]))

                    # Draw item count
                    self.menu.blit(font.render(str(self.hero.craft_available[index][0][1]), False, (255, 255, 255)),
                                   (3 + cell.x, 5 + cell.y - SIZE[1]))

                    # Draw outline
                    if index + 1 == self.hero.menu_pos:
                        pygame.draw.rect(self.menu, (255, 255, 255), (cell.x, cell.y + 2 - SIZE[1], cell.w, cell.h), 1)

            # Меню жизни
            self.hp_menu.fill((107, 105, 105))
            pygame.draw.rect(self.hp_menu, (215, 215, 215), (0, 0, self.hp_menu.get_width(), self.hp_menu.get_height()),
                             1)

            if self.hero.hp > 10:
                for n in range(1, round(10) + 1):
                    self.hp_menu.blit(self.hero.hp_img, (self.hp_menu.get_width() - n * 9 - 2, 2))
            else:
                for n in range(1, round(self.hero.hp) + 1):
                    self.hp_menu.blit(self.hero.hp_img, (self.hp_menu.get_width() - n * 9 - 2, 2))

            for n in range(1, round(self.hero.hunger) + 1):
                self.hp_menu.blit(self.hero.hunger_img, (self.hp_menu.get_width() - n * 9 - 2, 13))
            for n in range(1, round(self.hero.hp - 10) + 1):
                self.hp_menu.blit(self.hero.armor_img, (self.hp_menu.get_width() - n * 9 - 2, 2))

            # День & ночь
            if self.hero.hp <= 0:
                self.hero.dx = self.hero.dy = 0
                self.time += 2
                if self.time > 300:
                    if self.hero.spawn_point:
                        for item in [i for i in self.hero.inventory if i]:
                            self.pickup.append(PickUp(self.hero.x + randint(0, self.hero.rect.w),
                                                      self.hero.y + randint(0, self.hero.rect.h // 2),
                                                      item[0],
                                                      item[1]))
                        self.hero.x, self.hero.y = self.hero.spawn_point[-1]
                        self.hero.rect.x, self.hero.rect.y = self.hero.x, self.hero.y
                        self.hero.inventory = [None] * 20
                        self.hero.hp = self.hero.hunger = 10
                        self.time = 0
                    else:
                        self.game = False

            if (self.time > 180) and (self.hero.hp > 0):
                self.time_speed = -self.time_speed
                self.time = 180
            if self.time < 0:
                self.time_speed = -self.time_speed
                self.time = 0
            self.time += self.time_speed
            self.night.set_alpha(self.time)

            # Отображение на экране
            window.blit(self.screen, (0, 0))
            window.blit(self.night, (0, 0))
            window.blit(self.menu, (0, SIZE[1]))
            window.blit(self.hp_menu, (SIZE[0] - self.hp_menu.get_width(), 0))

            # Курсор
            if self.hero.inventory[self.hero.inventory_menu_pos - 1]:
                if type(links[self.hero.inventory[self.hero.inventory_menu_pos - 1][0]]) == list:
                    window.blit(
                        pygame.transform.scale(links[self.hero.inventory[self.hero.inventory_menu_pos - 1][0]][0],
                                               (18, 18)), (self.hero.cursor[0] - 10, self.hero.cursor[1] - 10))
                else:
                    window.blit(pygame.transform.scale(links[self.hero.inventory[self.hero.inventory_menu_pos - 1][0]],
                                                       (18, 18)), (self.hero.cursor[0] - 10, self.hero.cursor[1] - 10))
            else:
                pygame.draw.line(window, (0, 0, 0), (self.hero.cursor[0] - 5, self.hero.cursor[1] - 5),
                                 (self.hero.cursor[0] + 5, self.hero.cursor[1] + 5))
                pygame.draw.line(window, (0, 0, 0), (self.hero.cursor[0] - 5, self.hero.cursor[1] + 5),
                                 (self.hero.cursor[0] + 5, self.hero.cursor[1] - 5))

            # Описание предмета
            num = pygame.Rect(*self.hero.cursor, 1, 1).collidelist(inventory_cells)
            if num != -1:
                if self.hero.inventory[num]:
                    name = self.hero.inventory[num][0]

                    if name[-7:] == 'pickaxe':
                        text = description['pickaxe']
                    elif name[-3:] == 'axe':
                        text = description['axe']
                    elif name[-6:] == 'shovel':
                        text = description['shovel']
                    elif name[-5:] == 'sword':
                        text = description['sword']
                    elif name[-6:] == 'hammer':
                        text = description['hammer']
                    elif (name == 'iron_boots') or (name == 'iron_leggings') or (name == 'iron_chestplate') or \
                            (name == 'iron_helmet'):
                        text = description['armor']
                    elif name[-4:] == 'wall':
                        text = description['wall']
                    elif name[-3:] == 'ore':
                        text = description['ore']
                    elif name[-5:] == 'ingot':
                        text = description['ingot']
                    else:
                        text = description[name]

                    if self.hero.cursor[0] + 10 + font.size(text)[0] + 2 < SIZE[0]:
                        pygame.draw.rect(window, (107, 105, 105),
                                         (self.hero.cursor[0] + 10, self.hero.cursor[1] - 20,
                                          font.size(text)[0] + 2, 15))
                        pygame.draw.rect(window, (215, 215, 215),
                                         (self.hero.cursor[0] + 10, self.hero.cursor[1] - 20,
                                          font.size(text)[0] + 2, 15), 1)
                        window.blit(font.render(text, False, (255, 255, 255)),
                                    (self.hero.cursor[0] + 12, self.hero.cursor[1] - 18))
                    else:
                        pygame.draw.rect(window, (107, 105, 105),
                                         (self.hero.cursor[0] + 10, self.hero.cursor[1] - 20,
                                          -font.size(text)[0] - 2, 15))
                        pygame.draw.rect(window, (215, 215, 215),
                                         (self.hero.cursor[0] + 10, self.hero.cursor[1] - 20,
                                          -font.size(text)[0] - 2, 15), 1)
                        window.blit(font.render(text, False, (255, 255, 255)),
                                    (self.hero.cursor[0] + 10 - font.size(text)[0], self.hero.cursor[1] - 18))
                    del name, text
            else:
                # Стоимость крафта
                available = self.hero.furnace_available or self.hero.craft_available

                num = pygame.Rect(*self.hero.cursor, 1, 1).collidelist(menu_cells)
                if num != -1 and num < len(available):
                    num += max(0, self.hero.menu_pos - len(menu_cells))
                    if available[num]:
                        text = '| '
                        for unit in available[num][1]:
                            text += str(unit[1]) + ' ' + str(unit[0]).replace('_', ' ') + ' | '

                        pygame.draw.rect(window, (107, 105, 105), (self.hero.cursor[0] + 10,
                                                                   self.hero.cursor[1] - 20,
                                                                   font.size(text)[0] + 2, 15))
                        pygame.draw.rect(window, (215, 215, 215), (self.hero.cursor[0] + 10,
                                                                   self.hero.cursor[1] - 20,
                                                                   font.size(text)[0] + 2, 15), 1)
                        window.blit(font.render(text, False, (255, 255, 255)), (self.hero.cursor[0] + 12,
                                                                                self.hero.cursor[1] - 18))
                        del text
                del available

            # Счётчик FPS
            time_delta = (datetime.now() - time0).microseconds / 1000000
            window.blit(font.render(str(round(1 / time_delta)), False, (255, 255, 255)), (0, 0))

            # Обновление кадра
            pygame.display.flip()
            pygame.time.Clock().tick(150)

    def game_objects_render(self):
        for n in self.wall:
            n.render(self)
        for n in self.block:
            n.render(self)
        for n in self.block:
            if n.hp0 <= 0:
                n.destroy(game)
        for types in self.animals:
            for n in self.animals[types]:
                n.render(self)
        for n in self.pickup:
            n.render(self)
        for n in self.enemy:
            n.render(self)
        for n in self.arrow:
            n.render(self)
        self.hero.render(self)
        self.camera.render(self.hero.rect.centerx, self.hero.rect.centery)

    def key_read(self):
        for n in pygame.event.get():
            if n.type == pygame.QUIT:
                quit()
            if n.type == pygame.KEYDOWN:
                if n.key == pygame.K_w:
                    self.hero.up = True
                if n.key == pygame.K_a:
                    self.hero.left = True
                if n.key == pygame.K_d:
                    self.hero.right = True
                if n.key == pygame.K_s:
                    self.hero.down = True
                if n.key == pygame.K_DOWN:
                    self.hero.k_down = True
                if n.key == pygame.K_UP:
                    self.hero.k_up = True
                if n.key == pygame.K_LEFT:
                    self.hero.k_left = True
                if n.key == pygame.K_RIGHT:
                    self.hero.k_right = True
                if n.key == pygame.K_q:
                    self.hero.q = True
                if n.key == pygame.K_m:
                    self.map()
                    break
                if n.key == pygame.K_ESCAPE:
                    self.pause()
                    break
                if n.key == pygame.K_TAB:
                    self.inventory()
                    break
            if n.type == pygame.KEYUP:
                if n.key == pygame.K_w:
                    self.hero.up = False
                if n.key == pygame.K_a:
                    self.hero.left = False
                if n.key == pygame.K_d:
                    self.hero.right = False
                if n.key == pygame.K_s:
                    self.hero.down = False
            if n.type == pygame.MOUSEBUTTONDOWN:
                if n.button == 4:
                    self.hero.inventory_menu_pos -= 1
                if n.button == 5:
                    self.hero.inventory_menu_pos += 1

        if (self.hero.cooldown == self.hero.cooldown0) and pygame.mouse.get_pressed()[0]:
            self.hero.cooldown -= 1
            self.hero.left_click = True
        else:
            self.hero.left_click = False
        if (self.hero.cooldown == self.hero.cooldown0) and pygame.mouse.get_pressed()[2]:
            self.hero.right_click = True
            self.hero.cooldown -= 1
        else:
            self.hero.right_click = False

    def add_zombie(self):
        if 1 == randint(0, 1):
            _y = []
            for q in self.block:
                if q.Collision and (q.rect.x == round(self.camera.x / 25) * 25):
                    _y.append(q.rect.y)
            self.enemy.append(Zombie(self.camera.x, min(_y) - 25))
        else:
            _y = []
            for q in self.block:
                if q.Collision and (q.rect.x == round((self.camera.x + SIZE[0]) / 25) * 25):
                    _y.append(q.rect.y)
            self.enemy.append(Zombie(self.camera.x + SIZE[0], min(_y) - 25))

    def add_bird(self):
        _y = F_SIZE[1]
        for q in self.block:
            if q.Visible:
                if q.rect.y < _y:
                    _y = q.rect.y
        if _y - 25 > self.camera.y:
            _y = randint(self.camera.y, _y - 25)
            if 1 == randint(0, 1):
                _x = round(randint(round(self.hero.x) - SIZE[0] * 2, round(self.hero.x) - SIZE[0]) / 25) * 25
                self.animals['bird'].append(Bird(_x, _y, False))
            else:
                _x = round(randint(round(self.hero.x) + SIZE[0], round(self.hero.x) + SIZE[0] * 2) / 25) * 25
                self.animals['bird'].append(Bird(_x, _y, True))

    def add_sheep(self):
        if 1 == randint(0, 1):
            _y = []
            _x = round(randint(self.camera.x - SIZE[0] * 5, self.camera.x - 34) / 25) * 25
            if _x >= 0:
                for q in self.block:
                    if q.Collision and (q.rect.x == _x):
                        _y.append(q.rect.y)
                self.animals['sheep'].append(Sheep(_x, min(_y)))
                del _y, _x
        else:
            _y = []
            _x = round(randint(self.camera.x + SIZE[0], self.camera.x + SIZE[0] * 5) / 25) * 25
            if _x <= F_SIZE[0]:
                for q in self.block:
                    if q.Collision and (q.rect.x == _x):
                        _y.append(q.rect.y)
                self.animals['sheep'].append(Sheep(_x, min(_y)))
                del _y, _x

    def add_pig(self):
        if 1 == randint(0, 1):
            _y = []
            _x = round(randint(self.camera.x - SIZE[0] * 5, self.camera.x - 34) / 25) * 25
            if _x >= 0:
                for q in self.block:
                    if q.Collision and (q.rect.x == _x):
                        _y.append(q.rect.y)
                self.animals['pig'].append(Pig(_x, min(_y)))
        else:
            _y = []
            _x = round(randint(self.camera.x + SIZE[0], self.camera.x + SIZE[0] * 5) / 25) * 25
            if _x <= F_SIZE[0]:
                for q in self.block:
                    if q.Collision and (q.rect.x == _x):
                        _y.append(q.rect.y)
                self.animals['pig'].append(Pig(_x, min(_y)))

    def pause(self):
        img = pygame.image.frombuffer(pygame.image.tostring(window, 'RGBA'), (SIZE[0], SIZE[1] + 56), 'RGBA')
        font_pause = pygame.font.Font(r'data\font.ttf', 25)
        font_console = pygame.font.SysFont('serif', 20)

        buttons = [
            Button([SIZE[0] / 2, 100], 'Pause', 25, False),
            Button([SIZE[0] / 2, 230], 'Save game', 25),
            Button([SIZE[0] / 2, 360], 'Exit', 25)
        ]
        for b in buttons:
            b.size[0] = 200

        write_save_name = self.save_name[:-5]
        write_text = ''

        pause = True
        enter_name = False
        console = False
        cons = pygame.Surface(SIZE)
        cons.fill((0, 0, 0))
        cons.set_alpha(150)
        mouse_cooldown = 0
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE) and (enter_name is False):
                        self.hero.left = self.hero.right = self.hero.up = self.hero.down = \
                            self.hero.right_click = self.hero.left_click = False
                        pause = False
                    if (event.key == pygame.K_ESCAPE) and enter_name:
                        enter_name = False
                    if (event.key == pygame.K_1) and (
                            pygame.key.get_mods() & pygame.KMOD_ALT) and DEBUG:
                        console = not console
                        write_text = ''
                        continue
                    if enter_name:
                        for character in range(48, 123):
                            if pygame.key.name(event.key) == chr(character):
                                write_save_name += chr(character)
                        if event.key == pygame.K_BACKSPACE:
                            write_save_name = write_save_name[:-1]
                        if event.key == pygame.K_RETURN:
                            write_save_name += '.json'
                            write_save(write_save_name, self.hero, self.block, self.wall, self.animals,
                                       self.time, self.time_speed)
                            write_save_name = ''
                            enter_name = False
                    if console:
                        if event.key in [pygame.K_KP0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3,
                                         pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, pygame.K_KP7,
                                         pygame.K_KP8, pygame.K_KP9]:
                            write_text += event.unicode

                        if event.key == pygame.K_SPACE:
                            write_text += ' '
                        if (event.key == pygame.K_9) and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                            write_text += '('
                            continue
                        if (event.key == pygame.K_0) and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                            write_text += ')'
                            continue

                        if event.key in range(32, 127):
                            write_text += event.unicode

                        if event.key == pygame.K_BACKSPACE:
                            write_text = write_text[:-1]
                        if event.key == pygame.K_RETURN:
                            try:
                                exec(write_text)
                            except:
                                pass
                            write_text = ''

            mouse = pygame.mouse.get_pos()
            if mouse_cooldown == 0:
                is_pressed = pygame.mouse.get_pressed()[0]
                if is_pressed:
                    mouse_cooldown = 50
            else:
                mouse_cooldown -= 1
                is_pressed = False

            window.blit(img, (0, 0))

            for button in buttons:
                button.render(mouse)
                button.draw(window)
            if is_pressed:
                if buttons[1].hover and not enter_name and not console:
                    enter_name = True
                elif buttons[2].hover and not enter_name and not console:
                    self.game = False
                    pause = False

            if enter_name:
                pygame.draw.rect(window, (107, 105, 105), (SIZE[0] / 2 - 100, 390, 200, 46))
                pygame.draw.rect(window, (215, 215, 215), (SIZE[0] / 2 - 100, 390, 200, 46), 1)
                window.blit(font_pause.render(write_save_name, False, (255, 255, 255)),
                            (SIZE[0] / 2 - font_pause.size(write_save_name)[0] / 2, 397))

            if console:
                window.blit(cons, (0, 0))
                window.blit(font_console.render(write_text, False, (255, 255, 255)), (0, 0))

            window.blit(t_iron_pickaxe,
                        (pygame.mouse.get_pos()[0] - 10, pygame.mouse.get_pos()[1] - 10))

            pygame.display.flip()

    def map(self):
        img = pygame.image.frombuffer(pygame.image.tostring(window, 'RGBA'), (SIZE[0], SIZE[1] + 56), 'RGBA')

        pause = True

        sfrc = pygame.Surface([F_SIZE[0], F_SIZE[1]])
        sfrc.fill((14, 166, 241))

        for unit in self.wall + self.block:
            if unit.explored:
                for itm in minimap:
                    if unit.name == itm[1]:
                        pygame.draw.rect(sfrc, itm[0], (unit.rect.x, unit.rect.y, 25, 25))
                        if unit.name == 'door':
                            pygame.draw.rect(sfrc, itm[0], (unit.rect.x, unit.rect.y + 25, 25, 25))
            else:
                pygame.draw.rect(sfrc, (50, 50, 50), (unit.rect.x, unit.rect.y, 25, 25))

        pygame.draw.rect(sfrc, (255, 0, 0), (self.hero.x, self.hero.y, 25, 50))

        sfrc = pygame.transform.scale(sfrc, (SIZE[0], round(F_SIZE[1] / F_SIZE[0] * SIZE[0])))
        pygame.draw.rect(sfrc, (215, 215, 215), (0, 0, sfrc.get_width(), sfrc.get_height()), 1)

        sign = Button([SIZE[0] / 2, 80], 'Map', 25, False)

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.hero.left = self.hero.right = self.hero.up = self.hero.down = \
                            self.hero.right_click = self.hero.left_click = False
                        pause = False

            window.blit(img, (0, 0))
            sign.draw(window)
            window.blit(sfrc, (0, SIZE[1] / 4))

            window.blit(t_iron_pickaxe, (pygame.mouse.get_pos()[0] - 10, pygame.mouse.get_pos()[1] - 10))

            pygame.display.flip()

    def inventory(self, chest=None):
        img = pygame.image.frombuffer(pygame.image.tostring(window, 'RGBA'), (SIZE[0], SIZE[1] + 56), 'RGBA')

        pause = True

        inventory_cells = []
        chest_cells = []

        x, y = SIZE[0] / 2 - 35 * 5, SIZE[1] / 2 - 35 * 2
        for _ in range(20):
            inventory_cells.append(pygame.Rect(x + 3, y + 3, 29, 29))
            x += 35
            if x >= SIZE[0] / 2 + 35 * 5:
                x = SIZE[0] / 2 - 35 * 5
                y += 35

        if chest:
            x, y = SIZE[0] / 2 - 35 * 5, SIZE[1] / 2 + 35
            for _ in range(15):
                chest_cells.append(pygame.Rect(x + 3, y + 3, 29, 29))
                x += 35
                if x >= SIZE[0] / 2 + 35 * 5:
                    x = SIZE[0] / 2 - 35 * 2.5
                    y += 35

        drag_item = None
        drag_num = None

        signI = Button([SIZE[0] / 2, 180], 'Inventory', 25, False)
        signC = Button([SIZE[0] / 2, 180], 'Chest', 25, False)

        while pause:
            # Key event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        self.hero.left = self.hero.right = self.hero.up = self.hero.down = \
                            self.hero.right_click = self.hero.left_click = False
                        pause = False

            # Mouse drag
            if any(pygame.mouse.get_pressed()):
                if not drag_item:
                    num = pygame.Rect(*pygame.mouse.get_pos(), 1, 1).collidelist(inventory_cells)
                    if num != -1 and self.hero.inventory[num]:
                        drag_item = self.hero.inventory[num][:]
                        if pygame.mouse.get_pressed()[1]:
                            drag_item[1] = ceil(drag_item[1] / 2)
                        elif pygame.mouse.get_pressed()[2]:
                            drag_item[1] = 1
                        drag_num = [num, True]
                        self.hero.inventory[num][1] -= drag_item[1]
                    elif chest:
                        num2 = pygame.Rect(*pygame.mouse.get_pos(), 1, 1).collidelist(chest_cells)
                        if num2 != -1 and chest[num2]:
                            drag_item = chest[num2][:]
                            if pygame.mouse.get_pressed()[1]:
                                drag_item[1] = ceil(drag_item[1] / 2)
                            elif pygame.mouse.get_pressed()[2]:
                                drag_item[1] = 1
                            drag_num = [num2, False]
                            chest[num2][1] -= drag_item[1]
            else:
                if drag_item:
                    num = pygame.Rect(*pygame.mouse.get_pos(), 1, 1).collidelist(inventory_cells)
                    if num != -1:
                        # Inventory
                        if self.hero.inventory[num]:
                            if drag_item[0] == self.hero.inventory[num][0]:
                                # Add
                                self.hero.inventory[num][1] += drag_item[1]
                            else:
                                # Swap
                                if drag_num[1]:
                                    self.hero.inventory[drag_num[0]] = self.hero.inventory[num][:]
                                else:
                                    chest[drag_num[0]] = self.hero.inventory[num][:]

                                self.hero.inventory[num] = drag_item[:]
                        else:
                            # Place
                            self.hero.inventory[num] = drag_item[:]
                    else:
                        # Set back
                        if drag_num[1] and not chest:
                            if self.hero.inventory[drag_num[0]]:
                                self.hero.inventory[drag_num[0]][1] += drag_item[1]
                            else:
                                self.hero.inventory[drag_num[0]] = drag_item[:]

                        # Chest
                        if chest:
                            num2 = pygame.Rect(*pygame.mouse.get_pos(), 1, 1).collidelist(chest_cells)
                            if num2 != -1:
                                if chest[num2]:
                                    if drag_item[0] == chest[num2][0]:
                                        # Add
                                        chest[num2][1] += drag_item[1]
                                    else:
                                        # Swap
                                        if drag_num[1]:
                                            self.hero.inventory[drag_num[0]] = chest[num2][:]
                                        else:
                                            chest[drag_num[0]] = chest[num2][:]

                                        chest[num2] = drag_item[:]
                                else:
                                    # Place
                                    chest[num2] = drag_item[:]
                            else:
                                # Set back
                                if not drag_num[1]:
                                    if chest[drag_num[0]]:
                                        chest[drag_num[0]][1] += drag_item[1]
                                    else:
                                        chest[drag_num[0]] = drag_item[:]
                    drag_item = None
                    drag_num = None

            # Delete zero-items
            for index, it in enumerate(self.hero.inventory):
                if it and it[1] <= 0:
                    self.hero.inventory[index] = None
            if chest:
                for index, it in enumerate(chest):
                    if it and it[1] <= 0:
                        chest[index] = None

            window.blit(img, (0, 0))

            # Инфентарь
            if not chest:
                signI.draw(window)
            pygame.draw.rect(window, (107, 105, 105), (SIZE[0] / 2 - 35 * 5, SIZE[1] / 2 - 35 * 2, 35 * 10, 35 * 2))
            pygame.draw.rect(window, (215, 215, 215), (SIZE[0] / 2 - 35 * 5, SIZE[1] / 2 - 35 * 2, 35 * 10, 35 * 2), 1)

            for index, cell in enumerate(inventory_cells):
                pygame.draw.rect(window, (77, 70, 70)
                if cell.collidepoint(pygame.mouse.get_pos()) else (107, 105, 105), cell)
                pygame.draw.rect(window, (215, 215, 215), cell, 1)
                if self.hero.inventory[index]:
                    icon = pygame.transform.scale(links[self.hero.inventory[index][0]].copy(), (20, 20))
                    window.blit(icon, (cell.x + 4.5, cell.y + 4.5))
                    window.blit(font.render(str(self.hero.inventory[index][1]), False, (212, 212, 212)),
                                (cell.x + 4.5, cell.y + 4.5))

            # Ящик
            if chest:
                signC.draw(window)

                pygame.draw.rect(window, (107, 105, 105), (SIZE[0] / 2 - 35 * 5, SIZE[1] / 2 + 35, 35 * 10, 35 * 2))
                pygame.draw.rect(window, (215, 215, 215), (SIZE[0] / 2 - 35 * 5, SIZE[1] / 2 + 35, 35 * 10, 35 * 2), 1)

                for index, cell in enumerate(chest_cells):
                    pygame.draw.rect(window, (77, 70, 70)
                    if cell.collidepoint(pygame.mouse.get_pos()) else (107, 105, 105), cell)
                    pygame.draw.rect(window, (215, 215, 215), cell, 1)
                    if chest[index]:
                        icon = pygame.transform.scale(links[chest[index][0]].copy(), (20, 20))
                        window.blit(icon, (cell.x + 4.5, cell.y + 4.5))
                        window.blit(font.render(str(chest[index][1]), False, (212, 212, 212)),
                                    (cell.x + 4.5, cell.y + 4.5))

            # Курсор
            if drag_item:
                window.blit(links[drag_item[0]], (pygame.mouse.get_pos()[0] - 10, pygame.mouse.get_pos()[1] - 10))
                window.blit(font.render(str(drag_item[1]), False, (212, 212, 212)),
                            (pygame.mouse.get_pos()[0] - 10, pygame.mouse.get_pos()[1] - 10))
            else:
                pygame.draw.line(window, (0, 0, 0), (pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] - 5),
                                 (pygame.mouse.get_pos()[0] + 5, pygame.mouse.get_pos()[1] + 5))
                pygame.draw.line(window, (0, 0, 0), (pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] + 5),
                                 (pygame.mouse.get_pos()[0] + 5, pygame.mouse.get_pos()[1] - 5))

            pygame.display.flip()

    def main_menu(self):
        SIZE[1] += 56

        # Проверка сохранение игры
        saves = listdir(r'data\saves')
        remove_saves = []
        for save in saves:
            if save[-5:] != '.json':
                remove_saves.append(save)
        for r_save in remove_saves:
            saves.remove(r_save)

        # Создание мира
        self.screen = pygame.Surface((SIZE[0], SIZE[1] + 56))
        self.night = pygame.Surface(SIZE)
        self.camera = Camera()
        self.block = []
        self.wall = []

        font_menu0 = pygame.font.Font(r'data\font.ttf', 40)
        font_menu1 = pygame.font.Font(r'data\font.ttf', 25)

        menu = True
        play = key_bindings = load = delete = False

        buttons = {
            'mainMenu': [
                Button([SIZE[0] / 2, 100], 'Main menu', 25, False),
                Button([SIZE[0] / 2, 230], 'Play', 25),  
                Button([SIZE[0] / 2, 320], 'Key bindings', 25),
                Button([SIZE[0] / 2, 410], 'Exit', 25)
            ],
            'keyBindings': [
                Button([SIZE[0] / 2, 100], 'Key bindings', 25, False),
                Button([SIZE[0] / 2, 300], keyBindings, 25, False),
                Button([SIZE[0] / 2, 500], 'Back', 25)
            ],
            'play': [
                Button([SIZE[0] / 2, 100], 'Play', 25, False),
                Button([SIZE[0] / 2, 230], 'New game', 25),
                Button([SIZE[0] / 2, 320], 'Load game', 25),
                Button([SIZE[0] / 2, 410], 'Delete game', 25),
                Button([SIZE[0] / 2, 540], 'Back', 25)
            ],
            'load':
                [Button([SIZE[0] / 2, 100], 'Load game', 25, False)] +
                [Button([SIZE[0] / 2, 230 + 90 * count], saves[count][:-5], 25)
                    for count in range(0, len(saves))] + 
                [Button([SIZE[0] / 2, 270 + 90 * len(saves)], 'Back', 25)],
            'delete': 
                [Button([SIZE[0] / 2, 100], 'Delete game', 25, False)] +
                [Button([SIZE[0] / 2, 230 + 90 * count], saves[count][:-5], 25)
                    for count in range(0, len(saves))] + 
                [Button([SIZE[0] / 2, 270 + 90 * len(saves)], 'Back', 25)],
        }

        for i in buttons['mainMenu'] + buttons['play'] + buttons['load'] + buttons['delete']:
            i.size[0] = 200

        cam_dx = 1

        map_img = pygame.image.load(r'data\textures\menu map.png').convert_alpha()

        for x in range(map_img.get_width()):
            for y in range(map_img.get_height()):
                clr = map_img.get_at((x, y))
                for itm in minimap:
                    if itm[0] == clr:
                        if itm[1][-4:] == 'wall':
                            self.wall.append(Wall(x * 25, y * 25, itm[1], explored=True))
                        elif itm[1] == 'chest':
                            self.block.append(Block(x * 25, y * 25, itm[1], content=['eye_call', 1], explored=True))
                        else:
                            self.block.append(Block(x * 25, y * 25, itm[1], explored=True))

        mouse_cooldown = 0
        is_pressed = False
        while menu:
            # Обработка нажатий клавиш
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            mouse = pygame.mouse.get_pos()
            if mouse_cooldown == 0:
                is_pressed = pygame.mouse.get_pressed()[0]
                if is_pressed:
                    mouse_cooldown = 50
            else:
                mouse_cooldown -= 1
                is_pressed = False

            # Рендер
            self.screen.fill((14, 166, 241))

            self.camera.x += cam_dx
            if (self.camera.x + SIZE[0] > F_SIZE[0]) or (self.camera.x < 0):
                cam_dx *= -1

            for unit in self.block:
                unit.render(self)
            for unit in self.wall:
                unit.render(self)

            if not key_bindings and not play and not load and not delete:
                self.screen.blit(font_menu0.render('Terramine', False, (255, 255, 255)), (225, 10))

                for button in buttons['mainMenu']:
                    button.render(mouse)
                    button.draw(self.screen)

                if is_pressed:
                    if buttons['mainMenu'][1].hover:
                        play = True
                    elif buttons['mainMenu'][2].hover:
                        key_bindings = True
                    elif buttons['mainMenu'][3].hover:
                        exit()
            elif key_bindings:
                for button in buttons['keyBindings']:
                    button.render(mouse)
                    button.draw(self.screen)

                if is_pressed:
                    if buttons['keyBindings'][2].hover:
                        key_bindings = False
            elif play:
                for button in buttons['play']:
                    button.render(mouse)
                    button.draw(self.screen)

                if is_pressed:
                    if buttons['play'][1].hover:
                        save_name = ''
                        menu = False
                    elif buttons['play'][2].hover:
                        load = True
                        play = False
                    elif buttons['play'][3].hover:
                        delete = True
                        play = False
                    elif buttons['play'][4].hover:
                        play = False
            elif load:
                for button in buttons['load']:
                    button.render(mouse)
                    button.draw(self.screen)
                if is_pressed:
                    if buttons['load'][-1].hover:
                        load = False
                        play = True
                    for c in buttons['load'][1:-1]:
                        if c.hover:
                            save_name = c.text + '.json'
                            menu = False
                            break
            elif delete:
                for button in buttons['delete']:
                    button.render(mouse)
                    button.draw(self.screen)
                if is_pressed:
                    if buttons['delete'][-1].hover:
                        delete = False
                        play = True
                    for c in buttons['delete'][1:-1]:
                        if c.hover:
                            remove(r'data\saves\{name}'.format(name=c.text + '.json'))
                            saves.remove(c.text + '.json')
                            buttons['delete'].remove(c)
                            break

            # Курсор
            self.screen.blit(t_iron_pickaxe, (pygame.mouse.get_pos()[0] - 10, pygame.mouse.get_pos()[1] - 10))

            # Обновление экрана
            window.blit(self.screen, (0, 0))
            pygame.display.flip()

        SIZE[1] -= 56
        return save_name


# Окна меню
window = pygame.display.set_mode((SIZE[0], SIZE[1] + 56))
pygame.mouse.set_visible(False)

while True:
    game = Game()
    game.loop()
