import pygame

if __name__ == 'data.textures.loader':
    pygame.display.set_mode((700, 600))

    block = pygame.image.load(r'data\textures\block.png')
    items = pygame.image.load(r'data\textures\items.png')
    tools = pygame.image.load(r'data\textures\tools.png')
    wall = pygame.image.load(r'data\textures\wall.png')
    destroy = [pygame.image.load(r'data\textures\destroy.png').convert_alpha().subsurface(0, x * 25, 25, 25)
               for x in range(0, 8)]

    b_dirt = block.subsurface(0, 0, 25, 25).convert_alpha()
    b_cobblestone = block.subsurface(50, 0, 25, 25).convert_alpha()
    b_wood_planks = block.subsurface(75, 0, 25, 25).convert_alpha()
    b_log = block.subsurface(100, 0, 25, 25).convert_alpha()
    b_gold_ore = block.subsurface(125, 0, 25, 25).convert_alpha()
    b_iron_ore = block.subsurface(150, 0, 25, 25).convert_alpha()
    b_diamond_ore = block.subsurface(175, 0, 25, 25).convert_alpha()
    b_furnace = block.subsurface(200, 0, 25, 25).convert_alpha()
    b_sapling = block.subsurface(300, 0, 25, 25).convert_alpha()
    b_crafting_table = block.subsurface(325, 0, 25, 25).convert_alpha()
    b_ladder = block.subsurface(0, 25, 25, 25).convert_alpha()
    b_stone = block.subsurface(25, 0, 25, 25).convert_alpha()
    b_door0 = block.subsurface(46, 25, 4, 50).convert_alpha()
    b_door1 = block.subsurface(50, 25, 25, 50).convert_alpha()
    b_trapdoor0 = block.subsurface(75, 45, 25, 5).convert_alpha()
    b_trapdoor1 = block.subsurface(100, 25, 25, 25).convert_alpha()
    b_chest = block.subsurface(125, 25, 25, 25).convert_alpha()
    b_sand = block.subsurface(150, 25, 25, 25).convert_alpha()
    b_glass = block.subsurface(175, 25, 25, 25).convert_alpha()
    b_torch = block.subsurface(200, 25, 25, 25).convert_alpha()
    b_tall_grass = block.subsurface(225, 25, 25, 25).convert_alpha()
    b_bed = block.subsurface(275, 25, 50, 25).convert_alpha()
    b_grass = block.subsurface(225, 0, 25, 25).convert_alpha()
    b_leaves = block.subsurface(250, 0, 25, 25).convert_alpha()
    b_bedrock = block.subsurface(275, 0, 25, 25).convert_alpha()
    b_altar = block.subsurface(250, 25, 25, 25).convert_alpha()

    b_wheat = [block.subsurface(75, 50, 25, 25).convert_alpha(), block.subsurface(100, 50, 25, 25).convert_alpha(),
               block.subsurface(125, 50, 25, 25).convert_alpha(), block.subsurface(150, 50, 25, 25).convert_alpha(),
               block.subsurface(175, 50, 25, 25).convert_alpha(), block.subsurface(200, 50, 25, 25).convert_alpha(),
               block.subsurface(225, 50, 25, 25).convert_alpha(), block.subsurface(250, 50, 25, 25).convert_alpha()]
    b_mushroom = block.subsurface(275, 50, 25, 25).convert_alpha()
    b_wool = block.subsurface(325, 25, 25, 25).convert_alpha()
    b_fence = [block.subsurface(325, 50, 25, 25).convert_alpha(), block.subsurface(300, 50, 25, 25).convert_alpha()]

    i_gold_ingot = items.subsurface(0, 0, 20, 20).convert_alpha()
    i_iron_ingot = items.subsurface(20, 0, 20, 20).convert_alpha()
    i_diamond = items.subsurface(40, 0, 20, 20).convert_alpha()
    i_wheat = items.subsurface(60, 0, 20, 20).convert_alpha()
    i_wheat_seed = items.subsurface(80, 0, 20, 20).convert_alpha()
    i_bread = items.subsurface(100, 0, 20, 20).convert_alpha()
    i_iron_helmet = items.subsurface(120, 0, 20, 20).convert_alpha()
    i_iron_chestplate = items.subsurface(140, 0, 20, 20).convert_alpha()
    i_iron_leggings = items.subsurface(160, 0, 20, 20).convert_alpha()
    i_iron_boots = items.subsurface(180, 0, 20, 20).convert_alpha()
    i_eye_call = items.subsurface(0, 20, 20, 20).convert_alpha()
    i_mushroom_stew = items.subsurface(20, 20, 20, 20).convert_alpha()
    i_porkchop = items.subsurface(40, 20, 20, 20).convert_alpha()
    i_cooked_porkchop = items.subsurface(60, 20, 20, 20).convert_alpha()
    i_arrow = items.subsurface(80, 20, 20, 20).convert_alpha()
    i_fowl = items.subsurface(100, 20, 20, 20).convert_alpha()
    i_cooked_fowl = items.subsurface(120, 20, 20, 20).convert_alpha()
    i_mutton = items.subsurface(140, 20, 20, 20).convert_alpha()
    i_cooked_mutton = items.subsurface(160, 20, 20, 20).convert_alpha()
    i_thread = items.subsurface(180, 20, 20, 20).convert_alpha()
    i_stick = items.subsurface(0, 40, 20, 20).convert_alpha()
    i_scissors = items.subsurface(20, 40, 20, 20).convert_alpha()

    t_wooden_axe = tools.subsurface(0, 0, 20, 20).convert_alpha()
    t_wooden_pickaxe = tools.subsurface(0, 20, 20, 20).convert_alpha()
    t_wooden_shovel = tools.subsurface(0, 40, 20, 20).convert_alpha()
    t_wooden_sword = tools.subsurface(0, 60, 20, 20).convert_alpha()
    t_wooden_hammer = tools.subsurface(0, 80, 20, 20).convert_alpha()

    t_stone_axe = tools.subsurface(20, 0, 20, 20).convert_alpha()
    t_stone_pickaxe = tools.subsurface(20, 20, 20, 20).convert_alpha()
    t_stone_shovel = tools.subsurface(20, 40, 20, 20).convert_alpha()
    t_stone_sword = tools.subsurface(20, 60, 20, 20).convert_alpha()
    t_stone_hammer = tools.subsurface(20, 80, 20, 20).convert_alpha()

    t_iron_axe = tools.subsurface(40, 0, 20, 20).convert_alpha()
    t_iron_pickaxe = tools.subsurface(40, 20, 20, 20).convert_alpha()
    t_iron_shovel = tools.subsurface(40, 40, 20, 20).convert_alpha()
    t_iron_sword = tools.subsurface(40, 60, 20, 20).convert_alpha()
    t_iron_hammer = tools.subsurface(40, 80, 20, 20).convert_alpha()

    t_golden_axe = tools.subsurface(60, 0, 20, 20).convert_alpha()
    t_golden_pickaxe = tools.subsurface(60, 20, 20, 20).convert_alpha()
    t_golden_shovel = tools.subsurface(60, 40, 20, 20).convert_alpha()
    t_golden_sword = tools.subsurface(60, 60, 20, 20).convert_alpha()
    t_golden_hammer = tools.subsurface(60, 80, 20, 20).convert_alpha()

    t_diamond_axe = tools.subsurface(80, 0, 20, 20).convert_alpha()
    t_diamond_pickaxe = tools.subsurface(80, 20, 20, 20).convert_alpha()
    t_diamond_shovel = tools.subsurface(80, 40, 20, 20).convert_alpha()
    t_diamond_sword = tools.subsurface(80, 60, 20, 20).convert_alpha()
    t_diamond_hammer = tools.subsurface(80, 80, 20, 20).convert_alpha()

    t_bow = tools.subsurface(100, 0, 20, 20).convert_alpha()

    w_dirt = wall.subsurface(0, 0, 25, 25).convert_alpha()
    w_stone = wall.subsurface(25, 0, 25, 25).convert_alpha()
    w_cobblestone = wall.subsurface(50, 0, 25, 25).convert_alpha()
    w_wood_planks = wall.subsurface(75, 0, 25, 25).convert_alpha()
    w_log = wall.subsurface(100, 0, 25, 25).convert_alpha()
    w_sand = wall.subsurface(125, 0, 25, 25).convert_alpha()

    del block, items, tools, wall

    links = {
        'dirt': b_dirt,
        'cobblestone': b_cobblestone,
        'wood_planks': b_wood_planks,
        'log': b_log,
        'gold_ore': b_gold_ore,
        'iron_ore': b_iron_ore,
        'furnace': b_furnace,
        'sapling': b_sapling,
        'crafting_table': b_crafting_table,
        'ladder': b_ladder,
        'stone': b_stone,
        'door': [b_door1, b_door0],
        'trapdoor': [b_trapdoor1, b_trapdoor0],
        'chest': b_chest,
        'sand': b_sand,
        'glass': b_glass,
        'torch': b_torch,
        'tall_grass': b_tall_grass,
        'bed': b_bed,
        'wheat': b_wheat,
        'mushroom': b_mushroom,
        'gold_ingot': i_gold_ingot,
        'iron_ingot': i_iron_ingot,
        'diamond': i_diamond,
        'grown_wheat': i_wheat,
        'wheat_seed': i_wheat_seed,
        'bread': i_bread,
        'iron_helmet': i_iron_helmet,
        'iron_chestplate': i_iron_chestplate,
        'iron_leggings': i_iron_leggings,
        'iron_boots': i_iron_boots,
        'eye_call': i_eye_call,
        'mushroom_stew': i_mushroom_stew,
        'porkchop': i_porkchop,
        'arrow': i_arrow,
        'fowl': i_fowl,
        'wooden_axe': t_wooden_axe,
        'wooden_pickaxe': t_wooden_pickaxe,
        'wooden_shovel': t_wooden_shovel,
        'wooden_sword': t_wooden_sword,
        'wooden_hammer': t_wooden_hammer,
        'stone_axe': t_stone_axe,
        'stone_pickaxe': t_stone_pickaxe,
        'stone_shovel': t_stone_shovel,
        'stone_sword': t_stone_sword,
        'stone_hammer': t_stone_hammer,
        'iron_axe': t_iron_axe,
        'iron_pickaxe': t_iron_pickaxe,
        'iron_shovel': t_iron_shovel,
        'iron_sword': t_iron_sword,
        'iron_hammer': t_iron_hammer,
        'golden_axe': t_golden_axe,
        'golden_pickaxe': t_golden_pickaxe,
        'golden_shovel': t_golden_shovel,
        'golden_sword': t_golden_sword,
        'golden_hammer': t_golden_hammer,
        'diamond_axe': t_diamond_axe,
        'diamond_pickaxe': t_diamond_pickaxe,
        'diamond_shovel': t_diamond_shovel,
        'diamond_sword': t_diamond_sword,
        'diamond_hammer': t_diamond_hammer,
        'bow': t_bow,
        'dirt_wall': w_dirt,
        'stone_wall': w_stone,
        'cobblestone_wall': w_cobblestone,
        'wooden_wall': w_wood_planks,
        'log_wall': w_log,
        'sand_wall': w_sand,
        'iron_ore_wall': w_stone,
        'gold_ore_wall': w_stone,
        'diamond_ore_wall': w_stone,
        'grass_wall': w_dirt,
        'diamond_ore': b_diamond_ore,
        'grass': b_grass,
        'leaves': b_leaves,
        'bedrock': b_bedrock,
        'altar': b_altar,
        'cooked_fowl': i_cooked_fowl,
        'cooked_porkchop': i_cooked_porkchop,
        'mutton': i_mutton,
        'cooked_mutton': i_cooked_mutton,
        'wool': b_wool,
        'thread': i_thread,
        'stick': i_stick,
        'scissors': i_scissors,
        'fence': b_fence,
        'destroy': destroy
        }
