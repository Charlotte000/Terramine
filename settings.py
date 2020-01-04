SIZE = [700, 600]
F_SIZE = [10500, 1500]

DEBUG = True

trees = [
    lambda x, y: [[x, y, 'log'], [x, y - 25, 'log'], [x, y - 50, 'log'], [x, y - 75, 'log'],
                  [x - 25, y - 50, 'leaves'], [x + 25, y - 50, 'leaves'], [x - 25, y - 75, 'leaves'],
                  [x + 25, y - 75, 'leaves'], [x, y - 100, 'leaves']],
    lambda x, y: [[x, y, 'log'], [x, y - 25, 'log'], [x, y - 50, 'log'], [x, y - 75, 'log'], [x, y - 100, 'log'],
                  [x - 25, y - 50, 'leaves'], [x + 25, y - 50, 'leaves'], [x - 25, y - 75, 'leaves'],
                  [x + 25, y - 75, 'leaves'], [x, y - 125, 'leaves'], [x - 25, y - 100, 'leaves'],
                  [x + 25, y - 100, 'leaves'], [x - 25, y - 125, 'leaves'], [x + 25, y - 125, 'leaves'],
                  [x, y - 150, 'leaves'], [x - 50, y - 50, 'leaves'], [x + 50, y - 50, 'leaves'],
                  [x - 50, y - 75, 'leaves'], [x + 50, y - 75, 'leaves']],
    lambda x, y: [[x, y, 'log'], [x, y - 25, 'log'], [x, y - 50, 'log'], [x, y - 75, 'log'], [x, y - 100, 'log'],
                  [x, y - 125, 'log'], [x - 25, y - 100, 'leaves'], [x + 25, y - 100, 'leaves'],
                  [x - 25, y - 125, 'leaves'], [x + 25, y - 125, 'leaves'], [x, y - 150, 'leaves']]
]


# ----item----------------------price1-------------------price2------
craft_list = [
    [['wood_planks',      4], [['log',              1]]],
    [['crafting_table',   1], [['wood_planks',      4]]],
    [['stick',            4], [['wood_planks',      2]]],
    [['torch',            4], [['stick',            1], ['coal',   1]]]
]
crafting_table_list = [
    [['wooden_pickaxe',   1], [['wood_planks',      3], ['stick',  2]]],
    [['stone_pickaxe',    1], [['cobblestone',      3], ['stick',  2]]],
    [['iron_pickaxe',     1], [['iron_ingot',       3], ['stick',  2]]],
    [['golden_pickaxe',   1], [['gold_ingot',       3], ['stick',  2]]],
    [['diamond_pickaxe',  1], [['diamond',          3], ['stick',  2]]],

    [['wooden_axe',       1], [['wood_planks',      3], ['stick',  2]]],
    [['stone_axe',        1], [['cobblestone',      3], ['stick',  2]]],
    [['iron_axe',         1], [['iron_ingot',       3], ['stick',  2]]],
    [['golden_axe',       1], [['gold_ingot',       3], ['stick',  2]]],
    [['diamond_axe',      1], [['diamond',          3], ['stick',  2]]],

    [['wooden_shovel',    1], [['wood_planks',      1], ['stick',  2]]],
    [['stone_shovel',     1], [['cobblestone',      1], ['stick',  2]]],
    [['iron_shovel',      1], [['iron_ingot',       1], ['stick',  2]]],
    [['golden_shovel',    1], [['gold_ingot',       1], ['stick',  2]]],
    [['diamond_shovel',   1], [['diamond',          1], ['stick',  2]]],

    [['wooden_sword',     1], [['wood_planks',      2], ['stick',  1]]],
    [['stone_sword',      1], [['cobblestone',      2], ['stick',  1]]],
    [['iron_sword',       1], [['iron_ingot',       2], ['stick',  1]]],
    [['golden_sword',     1], [['gold_ingot',       2], ['stick',  1]]],
    [['diamond_sword',    1], [['diamond',          2], ['stick',  1]]],

    [['wooden_hammer',    1], [['wood_planks',      3], ['stick',  2]]],
    [['stone_hammer',     1], [['cobblestone',      3], ['stick',  2]]],
    [['iron_hammer',      1], [['iron_ingot',       3], ['stick',  2]]],
    [['golden_hammer',    1], [['gold_ingot',       3], ['stick',  2]]],
    [['diamond_hammer',   1], [['diamond',          3], ['stick',  2]]],

    [['iron_helmet',      1], [['iron_ingot',       5]]],
    [['iron_chestplate',  1], [['iron_ingot',       8]]],
    [['iron_leggings',    1], [['iron_ingot',       7]]],
    [['iron_boots',       1], [['iron_ingot',       4]]],

    [['wooden_wall',      4], [['wood_planks',      4]]],
    [['cobblestone_wall', 4], [['cobblestone',      4]]],
    [['log_wall',         4], [['log',              4]]],
    [['stone_wall',       4], [['stone',            4]]],

    [['furnace',          1], [['cobblestone',      8]]],
    [['ladder',           3], [['stick',            7]]],
    [['door',             1], [['wood_planks',      6]]],
    [['trapdoor',         2], [['wood_planks',      6]]],
    [['chest',            1], [['wood_planks',      8]]],
    [['bread',            1], [['grown_wheat',      3]]],
    [['bed',              1], [['wood_planks',      4], ['wool',   2]]],
    [['arrow',            4], [['stick',            2], ['thread', 1]]],
    [['bow',              1], [['stick',            4], ['thread', 3]]],
    [['thread',           4], [['wool',             1]]],
    [['scissors',         1], [['iron_ingot',       3]]],
    [['fence',            1], [['stick',            4]]]
]

furnace_list = [
    [['gold_ingot',       1], [['gold_ore',         1], ['coal',   1]]],
    [['iron_ingot',       1], [['iron_ore',         1], ['coal',   1]]],
    [['stone',            1], [['cobblestone',      1], ['coal',   1]]],
    [['glass',            1], [['sand',             1], ['coal',   1]]],
    [['mushroom_stew',    1], [['mushroom',         1], ['coal',   1]]],
    [['cooked_porkchop',  1], [['porkchop',         1], ['coal',   1]]],
    [['cooked_fowl',      1], [['fowl',             1], ['coal',   1]]],
    [['cooked_mutton',    1], [['mutton',           1], ['coal',   1]]],
    [['coal',             1], [['log',              2]]]
]

description = {
    'log': 'A log is used in crafting or building',
    'wood_planks': 'Wood planks is used in crafting or building',
    'dirt': 'The dirt can be used in building',
    'crafting_table': 'Crafting table on which you can craft more advanced things',
    'diamond': 'The rarest item in the game, which is used in crafting',
    'cobblestone': 'The cobblestone is used in building and can be melted into stone in the furnace',
    'stone': 'The stone is used in building',
    'torch': 'A torch illuminates around itself',
    'furnace': 'A furnace in which you will be able to melt the ore',
    'ladder': 'You can climb up or down the stairs',
    'door': 'A door can protect your home from enemies',
    'trapdoor': 'Trapdoor is the same as the door, only in the floor',
    'sapling': 'Sapling can be planted in the ground and it will grow into a tree',
    'sand': 'Sand can be used in construction or it can be melted into glass',
    'glass': 'Glass is used in building',
    'wheat_seed': 'Wheat seed can be planted in the ground and it will grow into wheat',
    'grown_wheat': 'From wheat you can make bread in the crafting table',
    'eye_call': 'This amulet is used for the altar to summon the boss',
    'chest': 'You can store things in the chest',
    'bread': 'Bread will fill your hunger and health',
    'bed': 'If you die you will appear in your bed',
    'mushroom': 'Mushrooms can be planted or stewed in the furnace',
    'mushroom_stew': 'Mushroom stew will fill your hunger and health',
    'porkchop': 'Porkchop can be roasted in the furnace',
    'cooked_porkchop': 'Cooked porkchop will fill your hunger and health',
    'arrow': 'Arrows are used in archery',
    'bow': 'You can shoot a bow using arrows',
    'fowl': 'Fowl can be roasted in the furnace',
    'cooked_fowl': 'Cooked fowl will fill your hunger and health',
    'mutton': 'Mutton can be roasted in the furnace',
    'cooked_mutton': 'Cooked mutton will fill your hunger and health',
    'wool': 'Wool is used in construction or in crafting threads',
    'thread': 'Threads are used in crafting',
    'stick': 'Sticks are used in crafting',
    'scissors': 'Is used for sheep shearing',
    'fence': 'Encloses animals',
    'coal': 'Coal is using in ore smelting in the furnace',

    'wall': 'Wall is a decor',
    'armor': 'Armor that will add the amount of health',
    'sword': 'The sword deals more damage to the enemy and pushes him away from you',
    'shovel': 'With a shovel you will quickly destroy blocks of land or sand',
    'axe': 'Axe produces faster wood and destroys woodwork',
    'pickaxe': 'Pickaxe quickly produces stone, ore and stone products',
    'hammer': 'Hammer will destroy the wall',
    'ore': 'The ore can be melted in the furnace and used in crafting',
    'ingot': 'Ingot is used in crafting'
}

minimap = [
    [(122, 122, 122), 'stone'],
    [(196, 112, 23), 'dirt'],
    [(255, 255, 0), 'gold_ore'],
    [(192, 158, 133), 'iron_ore'],
    [(0, 182, 255), 'diamond_ore'],
    [(68, 68, 68), 'coal_ore'],
    [(0, 174, 0), 'grass'],
    [(66, 255, 0), 'leaves'],
    [(153, 81, 9), 'log'],
    [(0, 0, 0), 'bedrock'],
    [(210, 204, 148), 'sand'],
    [(150, 173, 150), 'tall_grass'],
    [(255, 199, 48), 'altar'],
    [(167, 167, 167), 'cobblestone'],
    [(255, 135, 15), 'chest'],
    [(186, 151, 94), 'wood_planks'],
    [(186, 151, 94), 'door'],
    [(186, 151, 94), 'trapdoor'],
    [(186, 151, 94), 'fence'],
    [(176, 176, 176), 'furnace'],

    [(81, 81, 81), 'stone_wall'],
    [(158, 153, 112), 'sand_wall'],
    [(99, 78, 64), 'dirt_wall'],
    [(115, 115, 115), 'cobblestone_wall'],
    [(86, 86, 86), 'stone_wall'],
    [(126, 110, 83), 'wooden_wall'],
    [(41, 35, 26), 'log_wall']
]


# Tools damage
axe_damage = ['log', 'wood_planks', 'crafting_table', 'door', 'trapdoor', 'ladder', 'leaves', 'fence']
pickaxe_damage = ['stone', 'cobblestone', 'iron_ore', 'gold_ore', 'diamond_ore', 'furnace', 'coal_ore']
shovel_damage = ['dirt', 'grass', 'sand']

# Key bindings
keyBindings = [
    '[Q] - delete item',
    '[Esc] - pause',
    '[A, D] - walk',
    '[W] - jump',
    '[S] - move down',
    '[M] - map',
    '[TAB] - inventory'
]