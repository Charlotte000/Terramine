if __name__ == 'utils':
    from math import degrees, atan, sqrt
    from json import dump, loads
    from random import randint, choice, randrange, choices, uniform
    import pygame
    from opensimplex import OpenSimplex

    from classes.Block import Block
    from classes.Wall import Wall
    from classes.Pig import Pig
    from classes.Sheep import Sheep
    from classes.Bird import Bird

    from settings import F_SIZE, SIZE


    def angle_calc(x1, y1, x2, y2):
        if x1 < x2:
            return -degrees(atan((y1 - y2) / (x1 - x2))) - 180
        elif x1 > x2:
            return -degrees(atan((y1 - y2) / (x1 - x2)))
        elif x1 == x2:
            if y1 > y2:
                return 270
            else:
                return 90


    def write_save(name, hero, block, wall, animals, time, time_speed):
        load_text = {
            'hero': None,
            'block': [],
            'wall': [],
            'environment': {'time': time, 'direction': -1 if time_speed < 0 else 1},
            'animal': {'sheep': [], 'pig': []}
            }
        load_text['hero'] = {'x': hero.x, 'y': hero.y, 'hp': hero.hp, 'hunger': hero.hunger,
                             'inventory': hero.inventory, 'spawn_point': hero.spawn_point}

        for unit in block:
            load_text['block'] += [{'x': unit.rect.x, 'y': unit.rect.y, 'name': unit.name, 'collision': unit.Collision,
                                    'wall': unit.wall, 'content': unit.content, 'cooldown': unit.cooldown,
                                    'explored': unit.explored}]

        for unit in wall:
            load_text['wall'] += [{'x': unit.x, 'y': unit.y, 'name': unit.name, 'explored': unit.explored}]

        for type in animals:
            if type == 'sheep':
                for unit in animals['sheep']:
                    load_text['animal']['sheep'].append({'x': unit.rect.centerx, 'y': unit.rect.centery,
                                                         'grow_time0': unit.grow_time0})
            elif type == 'pig':
                for unit in animals['pig']:
                    load_text['animal']['pig'].append({'x': unit.rect.centerx, 'y': unit.rect.centery})

        with open('data\saves\{save}'.format(save=name), 'w') as file:
            dump(load_text, file)


    def read_save(name, hero, block, wall, animals, time, time_speed):
        with open('data\saves\{save}'.format(save=name), 'r') as file:
            load_text = loads(file.read())
        hero.x, hero.y = load_text['hero']['x'], load_text['hero']['y']
        hero.hp, hero.hunger = load_text['hero']['hp'], load_text['hero']['hunger']
        hero.spawn_point = load_text['hero']['spawn_point']

        hero.inventory = load_text['hero']['inventory']

        for unit in load_text['block']:
            block.append(Block(x=unit['x'], y=unit['y'], name=unit['name'], collision=unit['collision'],
                               wall=unit['wall'], content=unit['content'], cooldown=unit['cooldown'],
                               explored=unit['explored']))

        for unit in load_text['wall']:
            wall.append(Wall(x=unit['x'], y=unit['y'], name=unit['name'], explored=unit['explored']))

        for type0 in load_text['animal']:
            if type0 == 'sheep':
                for unit in load_text['animal']['sheep']:
                    animals['sheep'].append(Sheep(unit['x'], unit['y']))
                    animals['sheep'][-1].grow_time0 = unit['grow_time0']
            if type0 == 'pig':
                for unit in load_text['animal']['pig']:
                    animals['pig'].append(Pig(unit['x'], unit['y']))
            if type0 == 'bird':
                for unit in load_text['animal']['bird']:
                    animals['bird'].append(Bird(unit['x'], unit['y']))
        time[0] = load_text['environment']['time']
        time_speed[0] *= load_text['environment']['direction']

    def create_map(hero, block, wall):
        trees = [
            lambda x, y: [[x, y, 'log'], [x, y - 1, 'log'], [x, y - 2, 'log'], [x, y - 3, 'log'],
                          [x - 1, y - 2, 'leaves'], [x + 1, y - 2, 'leaves'], [x - 1, y - 3, 'leaves'],
                          [x + 1, y - 3, 'leaves'], [x, y - 4, 'leaves']],
            lambda x, y: [[x, y, 'log'], [x, y - 1, 'log'], [x, y - 2, 'log'], [x, y - 3, 'log'], [x, y - 4, 'log'],
                          [x - 1, y - 2, 'leaves'], [x + 1, y - 2, 'leaves'], [x - 1, y - 3, 'leaves'],
                          [x + 1, y - 3, 'leaves'], [x, y - 5, 'leaves'], [x - 1, y - 4, 'leaves'],
                          [x + 1, y - 4, 'leaves'], [x - 1, y - 5, 'leaves'], [x + 1, y - 5, 'leaves'],
                          [x, y - 6, 'leaves'], [x - 2, y - 2, 'leaves'], [x + 2, y - 2, 'leaves'],
                          [x - 2, y - 3, 'leaves'], [x + 2, y - 3, 'leaves']],
            lambda x, y: [[x, y, 'log'], [x, y - 1, 'log'], [x, y - 2, 'log'], [x, y - 3, 'log'], [x, y - 4, 'log'],
                          [x, y - 5, 'log'], [x - 1, y - 4, 'leaves'], [x + 1, y - 4, 'leaves'],
                          [x - 1, y - 5, 'leaves'], [x + 1, y - 5, 'leaves'], [x, y - 6, 'leaves']]
        ]
        win = pygame.Surface((int(F_SIZE[0] / 25), int(F_SIZE[1] / 25)))
        win.fill((100, 100, 255))
        w, h = win.get_size()
        gen = OpenSimplex()

        off0 = [uniform(0, 1024), uniform(0, 1024)]
        off1 = [uniform(0, 1024), uniform(0, 1024)]
        off2 = [uniform(0, 1024), uniform(0, 1024)]
        off3 = [uniform(0, 1024), uniform(0, 1024)]
        off4 = [uniform(0, 1024), uniform(0, 1024)]
        altarX = randint(10, w - 10)
        for x in range(w):
            y = int(h / 10 * 7 + gen.noise2d(off0[0] + x / 20, off0[1]) * h / 10 * 2)
            for i in range(y):
                if i > h / 10 * 7 + gen.noise2d(off1[0] + x / 10, off1[1]) * h / 10 * 2 - h / 8:
                    if gen.noise2d(off4[0] + x / 30, off4[1] + i / 30) > .3:
                        # Sand
                        win.set_at((x, h - i), (210, 204, 148))
                    else:
                        if i == y - 1:
                            # Grass
                            win.set_at((x, h - i), (0, 174, 0))
                            
                            # Tall grass
                            if uniform(0, 1) > .7:
                                win.set_at((x, h - i - 1), (150, 173, 150))
                                
                            # Tree
                            if uniform(0, 1) > .9:
                                for unit in choice(trees)(x, h - i - 1):
                                    if unit[2] == 'log':
                                        c = (153, 81, 9)
                                    elif unit[2] == 'leaves':
                                        c = (66, 255, 0)
                                    win.set_at((unit[0], unit[1]), c)
                        else:
                            # Dirt
                            win.set_at((x, h - i), (196, 112, 23))
                else:
                    # Stone
                    win.set_at((x, h - i), (122, 122, 122))
            # Add altar
            if x  - 1 == altarX:
                win.set_at((x - 1, h - i - 1), (255, 199, 48))
                win.set_at((x, h - i), (167, 167, 167))
                win.set_at((x - 1, h - i), (167, 167, 167))
                win.set_at((x - 2, h - i), (167, 167, 167))

        # Making holes
        for x in range(w):
            for y in range(h):
                if gen.noise2d(off1[0] + x / 10, off1[1] + y / 5) < -.3:
                    if win.get_at((x, y)) == (196, 112, 23):
                        # Dirt wall
                        win.set_at((x, y), (99, 78, 64))
                    elif win.get_at((x, y)) == (122, 122, 122):
                        # Stone wall
                        win.set_at((x, y), (81, 81, 81))
                    elif win.get_at((x, y)) == (210, 204, 148):
                        # Sand wall
                        win.set_at((x, y), (158, 153, 112))


        # Add chest
        x0, y0 = randint(5, w - 5), int(h / 10 * 4 + randint(h / 10, h / 10 * 3))
        for x, y in [[x0 - 1, y0], [x0, y0], [x0 + 1, y0], [x0 - 1, y0 - 1], [x0, y0 - 1], [x0 + 1, y0 - 1], [x0, y0 - 2], [x0 + 1, y0 - 2]]:
            if win.get_at((x, y)) == (196, 112, 23):
                # Dirt wall
                win.set_at((x, y), (99, 78, 64))
            elif win.get_at((x, y)) == (122, 122, 122):
                # Stone wall
                win.set_at((x, y), (81, 81, 81))
            elif win.get_at((x, y)) == (210, 204, 148):
                # Sand wall
                win.set_at((x, y), (158, 153, 112))

        for x, y in [[x0 - 1, y0], [x0, y0], [x0, y0], [x0 + 1, y0]]:
            # Cobblestone
            win.set_at((x, y), (167, 167, 167))
        # Chest
        win.set_at((x0, y0 - 1), (255, 135, 15))

        # Add ore
        off0 = [uniform(0, 1024), uniform(0, 1024)]
        off1 = [uniform(0, 1024), uniform(0, 1024)]
        off2 = [uniform(0, 1024), uniform(0, 1024)]
        off3 = [uniform(0, 1024), uniform(0, 1024)]
        for x in range(w):
            for y in range(h):
                if win.get_at((x, y)) == (122, 122, 122):
                    if gen.noise2d(off0[0] + x / 5, off0[1] + y / 5) > .5:
                        # Coal
                        win.set_at((x, y), (68, 68, 68))
                    if gen.noise2d(off1[0] + x / 5, off1[1] + y / 5) > .7:
                        # Iron
                        win.set_at((x, y), (192, 158, 133))
                    if gen.noise2d(off2[0] + x / 5, off2[1] + y / 5) > .7 and y > h / 20 * 15:
                        # Gold
                        win.set_at((x, y), (255, 255, 0))
                    if gen.noise2d(off3[0] + x / 5, off3[1] + y / 5) > .6 and y > h / 20 * 17:
                        # Diamond
                        win.set_at((x, y), (0, 182, 255))

        # Add bedrock
        for x in range(w):
            for y in range(0, randint(2, 4)):
                win.set_at((x, h - y), (0, 0, 0))


        # Add items to the world
        for x in range(w):
            isTop = True
            for y in range(h):
                color = win.get_at((x, y))
                if x == hero.x / 25 and isTop:
                    hero.y = y * 25 - 50
                if color == (210, 204, 148):
                    block.append(Block(x * 25, y * 25, 'sand', True, 'sand_wall', explored=isTop))
                    isTop = False
                elif color == (196, 112, 23):
                    block.append(Block(x * 25, y * 25, 'dirt', True, 'dirt_wall', explored=isTop))
                    isTop = False
                elif color == (122, 122, 122):
                    block.append(Block(x * 25, y * 25, 'stone', True, 'stone_wall', explored=isTop))
                    isTop = False
                elif color == (99, 78, 64):
                    wall.append(Wall(x * 25, y * 25, 'dirt_wall', explored=isTop))
                elif color == (81, 81, 81):
                    wall.append(Wall(x * 25, y * 25, 'stone_wall', explored=isTop))
                elif color == (158, 153, 112):
                    wall.append(Wall(x * 25, y * 25, 'sand_wall', explored=isTop))
                elif color == (68, 68, 68):
                    block.append(Block(x * 25, y * 25, 'coal_ore', True, 'stone_wall', explored=isTop))
                    isTop = False
                elif color == (192, 158, 133):
                    block.append(Block(x * 25, y * 25, 'iron_ore', True, 'stone_wall', explored=isTop))
                    isTop = False
                elif color == (255, 255, 0):
                    block.append(Block(x * 25, y * 25, 'gold_ore', True, 'stone_wall', explored=isTop))
                    isTop = False
                elif color == (0, 182, 255):
                    block.append(Block(x * 25, y * 25, 'diamond_ore', True, 'stone_wall', explored=isTop))
                    isTop = False
                elif color == (0, 0, 0):
                    block.append(Block(x * 25, y * 25, 'bedrock', True, explored=isTop))
                    isTop = False
                elif color == (0, 174, 0):
                    block.append(Block(x * 25, y * 25, 'grass', True, 'dirt_wall', explored=True))
                    isTop = False
                elif color == (150, 173, 150):
                    block.append(Block(x * 25, y * 25, 'tall_grass', False, explored=True))
                elif color == (153, 81, 9):
                    block.append(Block(x * 25, y * 25, 'log', False, explored=True))
                elif color == (66, 255, 0):
                    block.append(Block(x * 25, y * 25, 'leaves', False, explored=True))
                elif color == (167, 167, 167):
                    block.append(Block(x * 25, y * 25, 'cobblestone', True, explored=isTop))
                elif color == (255, 135, 15):
                    block.append(Block(x * 25, y * 25, 'chest', True, explored=isTop, content=[['eye_call', 1]]))
                elif color == (255, 199, 48):
                    block.append(Block(x * 25, y * 25, 'altar', True, explored=isTop))