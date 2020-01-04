if __name__ == 'utils':
    from math import degrees, atan, sqrt
    from json import dump, loads
    from random import randint, choice, randrange, choices
    import pygame
    from threading import Thread

    from classes.Block import Block
    from classes.Wall import Wall
    from classes.Pig import Pig
    from classes.Sheep import Sheep
    from classes.Bird import Bird

    from settings import F_SIZE, trees, SIZE


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


    def create_map(hero, block, wall, screen):
        def process():
            nonlocal progress
            # Создание террасы
            first_level_y = F_SIZE[1] // 2
            first_level_x = F_SIZE[0] // 2 + randint(35, 100) * 25
            second_level_y = first_level_y + randint(4, 6) * 25
            third_level_y = F_SIZE[1] - randint(1, 3) * 25

            cave_y = [[randrange(second_level_y, third_level_y, 25), randint(1, 5)]]

            for x in range(0, F_SIZE[0], 25):
                progress += 1
                if 1 == randint(0, 1):
                    first_level_y += randint(-1, 1) * 25

                if 1 == randint(0, 1):
                    second_level_y += randint(-1, 1) * 25

                if 1 == randint(0, 1):
                    third_level_y += randint(-1, 1) * 25

                if first_level_y < 400:
                    first_level_y = 425
                if first_level_y > 900:
                    first_level_y = 875

                if second_level_y < 400:
                    second_level_y = 425
                elif second_level_y > 1100:
                    second_level_y = 1075

                if third_level_y < F_SIZE[1] - 75:
                    third_level_y = F_SIZE[1] - 50
                elif third_level_y >= F_SIZE[1]:
                    third_level_y = F_SIZE[1] - 25

                cave_y.append([cave_y[-1][0] + randint(-1, 1) * 25, cave_y[-1][1] + randint(-1, 1)])
                if cave_y[-1][1] < -1:
                    cave_y[-1][1] = -1
                elif cave_y[-1][1] > 5:
                    cave_y[-1][1] = 5

                if cave_y[-1][0] < second_level_y:
                    cave_y[-1][0] = second_level_y
                elif cave_y[-1][0] + cave_y[-1][1] * 25 > third_level_y:
                    cave_y[-1][0] = third_level_y - cave_y[-1][1] * 25

                if second_level_y < first_level_y:
                    if 1 == randint(0, 5):
                        second_level_y += 25 * randint(1, 2)

                if x <= first_level_x:
                    if first_level_y < second_level_y:
                        if 1 == randint(0, 2):
                            block.append(Block(x, first_level_y - 50, 'tall_grass', explored=True))
                        block.append(Block(x, first_level_y - 25, 'grass', wall='dirt_wall', explored=True))

                    for y in range(first_level_y, second_level_y, 25):
                        block.append(Block(x, y, 'dirt', wall='dirt_wall'))
                else:
                    for y in range(first_level_y, second_level_y, 25):
                        block.append(Block(x, y, 'sand', wall='sand_wall', explored=True if y == first_level_y else False))

                for y in range(second_level_y, third_level_y, 25):
                    exp = False
                    if (y == second_level_y) and (y <= first_level_y):
                        exp = True
                    block.append(Block(x, y, 'stone', wall='stone_wall', explored=exp))

                for y in range(third_level_y, F_SIZE[1], 25):
                    block.append(Block(x, y, 'bedrock'))

            # Добавление алтаря
            _x = round(randint(25, F_SIZE[0] - 25) / 25) * 25
            _y = F_SIZE[1]
            for q in block:
                progress += 1
                if q.Collision and (q.rect.x == _x):
                    if q.rect.y < _y:
                        _y = q.rect.y
            for q in block:
                progress += 1
                if (q.rect.x == _x) and (q.rect.y == _y - 25):
                    block.remove(q)
                elif (q.rect.x == _x - 25) and (q.rect.y == _y - 25):
                    block.remove(q)
                elif (q.rect.x == _x + 25) and (q.rect.y == _y - 25):
                    block.remove(q)
                elif (q.rect.x == _x) and (q.rect.y == _y - 50):
                    block.remove(q)

            block.append(Block(_x, _y - 25, 'cobblestone', explored=True))
            block.append(Block(_x - 25, _y - 25, 'cobblestone', explored=True))
            block.append(Block(_x + 25, _y - 25, 'cobblestone', explored=True))
            block.append(Block(_x, _y - 50, 'altar', collision=False, explored=True))

            _x = round(randint(25, F_SIZE[0] - 25) / 25) * 25
            _y = round(randint(F_SIZE[1] - 400, F_SIZE[1] - 125) / 25) * 25

            dead_block = []

            # Добавление пещер и ящика
            for q in block:
                progress += 1
                if (q.rect.x == _x) and (q.rect.y == _y):
                    dead_block.append(q)
                elif (q.rect.x == _x) and (q.rect.y == _y + 25):
                    dead_block.append(q)
                elif (q.rect.x == _x - 25) and (q.rect.y == _y + 25):
                    dead_block.append(q)
                elif (q.rect.x == _x + 25) and (q.rect.y == _y + 25):
                    dead_block.append(q)
                elif (q.rect.x == _x - 25) and (q.rect.y == _y):
                    dead_block.append(q)
                elif (q.rect.x == _x + 25) and (q.rect.y == _y):
                    dead_block.append(q)
                elif (q.rect.x == _x) and (q.rect.y == _y - 25):
                    dead_block.append(q)
                elif (q.rect.x == _x + 25) and (q.rect.y == _y - 25):
                    dead_block.append(q)
            block.append(Block(_x, _y, 'chest', collision=False, content=[['eye_call', 1]]))
            block.append(Block(_x, _y + 25, 'cobblestone', wall='stone_wall'))
            block.append(Block(_x - 25, _y + 25, 'cobblestone', wall='stone_wall'))
            block.append(Block(_x + 25, _y + 25, 'cobblestone', wall='stone_wall'))
            wall.append(Wall(_x, _y - 25, 'stone_wall'))
            wall.append(Wall(_x + 25, _y - 25, 'stone_wall'))
            wall.append(Wall(_x + 25, _y, 'stone_wall'))
            wall.append(Wall(_x - 25, _y, 'stone_wall'))
            wall.append(Wall(_x, _y, 'stone_wall'))

            for x, cave in enumerate(cave_y):
                progress += 1
                for y in range(cave[0], cave[0] + 25 * cave[1], 25):
                    for q in block:
                        if (q.rect.x == x * 25) and (q.rect.y == y) and (q.name != 'chest'):
                            dead_block.append(q)
                    wall.append(Wall(x * 25, y, 'stone_wall'))

            #  Удаление лишнего
            for q in set(dead_block):
                progress += 1
                block.remove(q)
            dead_block.clear()

            # Добваление ущелья
            center_x = first_level_x
            w_left, w_right = randint(10, 20), randint(10, 20)
            for y in range(0, F_SIZE[1], 25):
                progress += 1
                for x in range(center_x - w_left * 25, center_x + w_right * 25, 25):
                    for n in block:
                        if n.rect.x == x and n.rect.y == y and n.name != 'altar' and n.name != 'bedrock':
                            wall.append(Wall(n.rect.x, n.rect.y, 'stone_wall', explored=True))
                            dead_block.append(n)
                    for w in wall:
                        if w.rect.x == x and w.rect.y == y and not w.explored:
                            w.explored = True

                for n in block:
                    if n.rect.y == y:
                        if n.rect.x == center_x - (w_left + 1) * 25:
                            n.explored = True
                        if n.rect.x == center_x + w_right * 25:
                            n.explored = True
                w_left += randint(-1, 1)
                w_right -= randint(-1, 1)

            #  Удаление лишнего
            for q in set(dead_block):
                progress += 1
                block.remove(q)
            dead_block.clear()

            # Добавление руд
            for b in choices([i for i in block if i.name == 'stone'], k=randint(50, 200)):
                progress += 1
                dead_block.append(b)
                block.append(Block(b.rect.x, b.rect.y, 'iron_ore', wall='stone_wall'))

            for b in choices([i for i in block if i.name == 'stone'], k=randint(150, 250)):
                dead_block.append(b)
                block.append(Block(b.rect.x, b.rect.y, 'coal_ore', wall='stone_wall'))

            for b in choices([i for i in block if i.name == 'stone' and i.rect.y > 1100], k=randint(50, 100)):
                progress += 1
                dead_block.append(b)
                block.append(Block(b.rect.x, b.rect.y, 'gold_ore', wall='stone_wall'))

            for b in choices([i for i in block if i.name == 'stone' and i.rect.y > 1300], k=randint(30, 50)):
                progress += 1
                dead_block.append(b)
                block.append(Block(b.rect.x, b.rect.y, 'diamond_ore', wall='stone_wall'))

            # Добавление деревьев
            for x in [randrange(25, F_SIZE[0] - 25, 25) for _ in range(randint(50, 100))]:
                progress += 1
                y = min([n.rect.y for n in [i for i in block if i.rect.x == x]])
                for n in block:
                    if n.rect.x == x and n.rect.y == y and (n.name == 'grass' or n.name == 'dirt'):
                        for unit in choice(trees)(x, y - 25):
                            block.append(Block(unit[0], unit[1], unit[2], collision=False, explored=True))
                        break

            # Удаление лишнего
            for q in set(dead_block):
                progress += 1
                block.remove(q)

            # Установка координаты персонажа
            _y = F_SIZE[1]
            for unit in block:
                progress += 1
                if unit.Collision and (unit.rect.x == round(hero.x / 25) * 25):
                    if unit.rect.y < _y:
                        _y = unit.rect.y
            hero.y = _y - 50

        progress = 0
        t = Thread(target=process)
        t.start()

        while t.isAlive():
            w = progress / 50355 * 200
            if w > 200:
                w = 200
            pygame.draw.rect(screen, (107, 105, 105), (SIZE[0] / 2 - 100, 255, w, 10))
            pygame.draw.rect(screen, (215, 215, 215), (SIZE[0] / 2 - 100, 255, 200, 10), 1)
            pygame.event.get()
            pygame.display.flip()
