from worlds.generic.Rules import set_rule, add_rule
from BaseClasses import CollectionState
from typing import TYPE_CHECKING
from .Options import UndertaleYellowOptions

if TYPE_CHECKING:
    from . import UndertaleYellowWorld


def _undertale_is_route(world: "UndertaleYellowWorld", route: int):
    if route == 3:
        return world.options.route_required.current_key == "all_routes"
    if world.options.route_required.current_key == "all_routes":
        return True
    if route == 0:
        return world.options.route_required.current_key == "neutral"
    if route == 1:
        return world.options.route_required.current_key == "pacifist"
    if route == 2:
        return world.options.route_required.current_key == "genocide"
    return False

def _undertale_is_love_rando(world: "UndertaleYellowWorld", rando_love: bool):
    if world.options.rando_love:
        return rando_love == True
    else:
        return rando_love == False
def _undertale_is_stats_rando(world: "UndertaleYellowWorld", rando_stats: bool):
    if world.options.rando_stats:
        return rando_stats == True
    else:
        return rando_stats == False

def _undertale_can_level(exp: int, lvl: int):
    if exp >= 10 and lvl == 1:
        return True
    elif exp >= 30 and lvl == 2:
        return True
    elif exp >= 70 and lvl == 3:
        return True
    elif exp >= 120 and lvl == 4:
        return True
    elif exp >= 200 and lvl == 5:
        return True
    elif exp >= 300 and lvl == 6:
        return True
    elif exp >= 500 and lvl == 7:
        return True
    elif exp >= 800 and lvl == 8:
        return True
    elif exp >= 1200 and lvl == 9:
        return True
    elif exp >= 1700 and lvl == 10:
        return True
    elif exp >= 2500 and lvl == 11:
        return True
    elif exp >= 3500 and lvl == 12:
        return True
    elif exp >= 5000 and lvl == 13:
        return True
    elif exp >= 7000 and lvl == 14:
        return True
    elif exp >= 10000 and lvl == 15:
        return True
    elif exp >= 15000 and lvl == 16:
        return True
    elif exp >= 25000 and lvl == 17:
        return True
    elif exp >= 50000 and lvl == 18:
        return True
    elif exp >= 99999 and lvl == 19:
        return True
    return False


# Sets rules on entrances and advancements that are always applied
def set_rules(world: "UndertaleYellowWorld"):
    player = world.player
    multiworld = world.multiworld
    set_rule(multiworld.get_entrance("Ruins Hub", player), lambda state: state.has("Ruins Key", player))
    set_rule(multiworld.get_entrance("Snowdin Hub", player), lambda state: state.has("Snowdin Key", player))
    set_rule(multiworld.get_entrance("Dunes Hub", player), lambda state: state.has("Dunes Key", player))
    set_rule(multiworld.get_entrance("Steamworks Hub", player), lambda state: state.has("Steamworks Key", player))
    set_rule(multiworld.get_entrance("Hotland Hub", player), lambda state: state.has("Hotland Key", player))
    set_rule(multiworld.get_entrance("Dunes East Entrance", player),
             lambda state: state.has("Pickaxe", player))
    if _undertale_is_route(world, 1) and not  _undertale_is_route(world, 3):
        set_rule(multiworld.get_entrance("New Home Entrance", player),
                 lambda state: state.has("Left UG Apartment Roof Pass", player) and state.has(
                     "Right UG Apartment Roof Pass", player) and state.has("Steamworks Key", player) and state.has("Dunes Key", player))
    elif _undertale_is_route(world, 2) and not _undertale_is_route(world, 3):
        if _undertale_is_stats_rando(world, rando_stats=True):
            set_rule(multiworld.get_entrance("New Home Entrance", player),
                     lambda state: state.has("Left UG Apartment Roof Pass", player) and state.has(
                        "Right UG Apartment Roof Pass", player) and state.has("ATK Up", player, 18) and state.has("HP Up", player, 18) and state.has("ITEM", player))
        elif _undertale_is_stats_rando(world, rando_stats= False) and _undertale_is_love_rando(world, rando_love= True):
            set_rule(multiworld.get_entrance("New Home Entrance", player),
                    lambda state: state.has("Left UG Apartment Roof Pass", player) and state.has(
                        "Right UG Apartment Roof Pass", player) and state.has("LOVE", player, 18) and state.has("ITEM", player))
        else:
            set_rule(multiworld.get_entrance("New Home Entrance", player),
                     lambda state: state.has("Left UG Apartment Roof Pass", player) and state.has(
                         "Right UG Apartment Roof Pass", player) and state.has("Steamworks Key", player) and state.has("Dunes Key", player) and state.has("Hydrochloric Acid", player) and state.has("ITEM", player))
    elif _undertale_is_route(world, 3):
        if _undertale_is_stats_rando(world, rando_stats=True):
            set_rule(multiworld.get_entrance("New Home Entrance", player),
                    lambda state: state.has("Left UG Apartment Roof Pass", player) and state.has(
                        "Right UG Apartment Roof Pass", player) and state.has("ATK Up", player, 18) and state.has("HP Up", player, 18) and state.has("ITEM", player) or (state.has("Steamworks Key", player) and state.has("Dunes Key", player)) and state.has("Left UG Apartment Roof Pass", player) and state.has(
                        "Right UG Apartment Roof Pass", player))
        elif _undertale_is_stats_rando(world, rando_stats= False) and _undertale_is_love_rando(world, rando_love= True):
            set_rule(multiworld.get_entrance("New Home Entrance", player),
                    lambda state: state.has("Left UG Apartment Roof Pass", player) and state.has(
                        "Right UG Apartment Roof Pass", player) and state.has("LOVE", player, 18) and state.has("ITEM", player) or state.has("Steamworks Key", player) and state.has("Dunes Key", player) and state.has("Left UG Apartment Roof Pass", player) and state.has("Right UG Apartment Roof Pass", player))
        else:
            set_rule(multiworld.get_entrance("New Home Entrance", player),
                     lambda state: state.has("Left UG Apartment Roof Pass", player) and state.has(
                         "Right UG Apartment Roof Pass", player) and state.has("Steamworks Key", player) and state.has(
                         "Dunes Key", player))
    else:
        set_rule(multiworld.get_entrance("New Home Entrance", player),
                 lambda state: state.has("Left UG Apartment Roof Pass", player) and state.has(
                     "Right UG Apartment Roof Pass", player))
    if _undertale_is_stats_rando(world, rando_stats=True):
        if _undertale_is_route(world, route= 2) and (not _undertale_is_route(world, route= 3)):
            set_rule(multiworld.get_entrance("Wild East Entrance", player),
                     lambda state: state.has("ATK Up", player, 9) and state.has("HP Up", player, 9))
    elif _undertale_is_stats_rando(world, rando_stats=False) and _undertale_is_love_rando(world, rando_love=True):
        if _undertale_is_route(world, route= 2) and (not _undertale_is_route(world, route= 3)):
            set_rule(multiworld.get_entrance("Wild East Entrance", player),
                     lambda state: state.has("LOVE", player, 9))
    set_rule(multiworld.get_location("Steamworks: Golden Bandana", player),
            lambda state: state.has("Golden Pear", player) and state.has("Golden Coffee", player) and state.has("Golden Cactus", player))
    if _undertale_is_route(world, 1):
        set_rule(multiworld.get_entrance("Ketsukane Manor Entrance", player),
                 lambda state: state.has("Steamworks Key",player)),
        set_rule(multiworld.get_location("Ketsukane Manor: Ceroba's Fridge", player),
                 lambda state: state.can_reach("Ketsukane Manor", "Region", player)),
        set_rule(multiworld.get_location("Ketsukane Manor: Hidden Tape", player),
                 lambda state: state.can_reach("Ketsukane Manor", "Region", player)),
        set_rule(multiworld.get_location("Steamworks Pacifist: Trash Can Beef Jerky", player),
                 lambda state: state.can_reach("Steamworks Pacifist", "Region", player))
    if _undertale_is_route(world, 0):
        set_rule(multiworld.get_location("Steamworks Neutral: Cake", player),
                 lambda state: state.can_reach("Steamworks Neutral", "Region", player)),
        set_rule(multiworld.get_location("Steamworks Exit: Neutral Friendliness Pellets", player),
                 lambda state: state.can_reach("Steamworks Axis", "Region", player) and state.has("Hydrochloric Acid", player))
    if _undertale_is_route(world, route=0) and not _undertale_is_route(world, route=3):
        set_rule(multiworld.get_location("Steamworks Exit: Broken Vending Machine", player),
                 lambda state: state.can_reach("Steamworks Axis", "Region", player) and state.has("Hydrochloric Acid", player))
        set_rule(multiworld.get_location("Axis Pacifist/Neutral Victory", player),
                 lambda state: state.can_reach("Steamworks Axis", "Region", player) and state.has("Hydrochloric Acid", player))
    if _undertale_is_route(world, 2):
        if _undertale_is_stats_rando(world, rando_stats=True):
            set_rule(multiworld.get_location("Martlet Genocide Victory", player),
                     lambda state: state.can_reach("Snowdin", "Region", player) and state.has("HP Up", player, 6) and state.has("ATK Up", player, 6))
            set_rule(multiworld.get_location("Wild East: Dunes Barkeep 2", player),
                    lambda state: state.can_reach("Wild East", "Region", player) and state.has("HP Up", player, 9) and state.has("ATK Up", player, 9))
            set_rule(multiworld.get_location("Wild East: Genocide Friendliness Pellets", player),
                    lambda state: state.can_reach("Wild East", "Region", player) and state.has("HP Up", player, 9) and state.has("ATK Up", player, 9))
            set_rule(multiworld.get_location("Ceroba Genocide Victory", player),
                    lambda state: state.can_reach("Wild East", "Region", player) and state.has("HP Up", player, 9) and state.has("ATK Up", player, 9))
            set_rule(multiworld.get_location("Axis Genocide Victory", player),
                    lambda state: state.can_reach("Steamworks Axis", "Region", player) and state.has("HP Up", player, 11) and state.has("Hydrochloric Acid", player))
        elif _undertale_is_stats_rando(world, rando_stats=False) and _undertale_is_love_rando(world, rando_love=True):
            set_rule(multiworld.get_location("Martlet Genocide Victory", player),
                     lambda state: state.can_reach("Snowdin", "Region", player) and state.has("LOVE", player, 6))
            set_rule(multiworld.get_location("Wild East: Dunes Barkeep 2", player),
                    lambda state: state.can_reach("Wild East", "Region", player) and state.has("LOVE", player, 9))
            set_rule(multiworld.get_location("Wild East: Genocide Friendliness Pellets", player),
                    lambda state: state.can_reach("Wild East", "Region", player) and state.has("LOVE", player, 9))
            set_rule(multiworld.get_location("Ceroba Genocide Victory", player),
                    lambda state: state.can_reach("Wild East", "Region", player) and state.has("LOVE", player, 9))
            set_rule(multiworld.get_location("Axis Genocide Victory", player),
                    lambda state: state.can_reach("Steamworks Axis", "Region", player) and state.has("LOVE", player, 11) and state.has("Hydrochloric Acid", player))
        else:
            set_rule(multiworld.get_location("Martlet Genocide Victory", player),
                     lambda state: state.can_reach("Snowdin", "Region", player))
            set_rule(multiworld.get_location("Wild East: Dunes Barkeep 2", player),
                    lambda state: state.can_reach("Wild East", "Region", player)),
            set_rule(multiworld.get_location("Wild East: Genocide Friendliness Pellets", player),
                    lambda state: state.can_reach("Wild East", "Region", player))
            set_rule(multiworld.get_location("Axis Genocide Victory", player),
                    lambda state: state.can_reach("Steamworks Axis", "Region", player) and state.has("Hydrochloric Acid", player))
    if (_undertale_is_route(world, 0) or _undertale_is_route(world, 2)) and not _undertale_is_route(world, 3):
        set_rule(multiworld.get_location("Steamworks Exit: Broken Vending Machine", player),
                lambda state: state.can_reach("Steamworks Axis", "Region", player) and state.has("Hydrochloric Acid", player)),
    if (not _undertale_is_route(world, 2)) or _undertale_is_route(world, 3):
        set_rule(multiworld.get_location("Wild East: Broken Necklace", player),
                lambda state: state.can_reach("Wild East", "Region", player))
        set_rule(multiworld.get_location("Snowdin: Coffee Trade", player),
                 lambda state: state.has("Hndw Coffee", player)),
        set_rule(multiworld.get_location("Snowdin: Mitten Trade", player),
                 lambda state: state.has("Soggy Mitten", player)),
        set_rule(multiworld.get_location("Snowdin: Map Trade", player),
                 lambda state: state.has("Snowdin Map", player)),
        set_rule(multiworld.get_location("Snowdin: Matches Trade", player),
                 lambda state: state.has("Matches", player) and state.has("Hndw Coffee", player)),
        set_rule(multiworld.get_location("Snowdin: Scarf Trade", player),
                 lambda state: state.has("Lukewarm Coffee", player)),
    if (not _undertale_is_route(world, 0)) or _undertale_is_route(world, 3):
        set_rule(multiworld.get_location("New Home: Bench Chisps", player),
                lambda state: state.can_reach("New Home", "Region", player)),
    if (not _undertale_is_route(world, 1)) or _undertale_is_route(world, 3):
        set_rule(multiworld.get_location("Steamworks Neutral: Closet Water", player),
                lambda state: state.can_reach("Steamworks Neutral", "Region", player)),
    if _undertale_is_route(world, 2) and \
            (bool(world.options.rando_love.value) or bool(world.options.rando_stats.value)):
        maxlv = 1
        exp = 168
        curarea = "Ruins"

        while maxlv < 20:
            maxlv += 1
            if world.options.rando_love:
                set_rule(multiworld.get_location(("LOVE " + str(maxlv)), player), lambda state: False)
            if world.options.rando_stats:
                set_rule(multiworld.get_location(("ATK "+str(maxlv)), player), lambda state: False)
                set_rule(multiworld.get_location(("HP "+str(maxlv)), player), lambda state: False)
                if maxlv in {5, 9, 13, 17}:
                    set_rule(multiworld.get_location(("DEF "+str(maxlv)), player), lambda state: False)
        maxlv = 1
        while maxlv < 20:
            while _undertale_can_level(exp, maxlv):
                maxlv += 1
                if world.options.rando_stats:
                    if curarea == "Ruins":
                        add_rule(multiworld.get_location(("ATK "+str(maxlv)), player),
                                 lambda state: (state.can_reach("Ruins", "Region", player)), combine="or")
                        add_rule(multiworld.get_location(("HP "+str(maxlv)), player),
                                 lambda state: (state.can_reach("Ruins", "Region", player)), combine="or")
                        if maxlv == 5 or maxlv == 9 or maxlv == 13 or maxlv == 17:
                            add_rule(multiworld.get_location(("DEF "+str(maxlv)), player),
                                     lambda state: (state.can_reach("Ruins", "Region", player)), combine="or")
                    elif curarea == "Snowdin":
                        add_rule(multiworld.get_location(("ATK "+str(maxlv)), player),
                                 lambda state: (state.can_reach("Snowdin", "Region", player)), combine="or")
                        add_rule(multiworld.get_location(("HP "+str(maxlv)), player),
                                 lambda state: (state.can_reach("Snowdin", "Region", player)), combine="or")
                        if maxlv == 5 or maxlv == 9 or maxlv == 13 or maxlv == 17:
                            add_rule(multiworld.get_location(("DEF "+str(maxlv)), player),
                                     lambda state: (state.can_reach("Snowdin", "Region", player)), combine="or")
                    elif curarea == "Dunes West":
                        add_rule(multiworld.get_location(("ATK "+str(maxlv)), player),
                                 lambda state: (state.can_reach("Dunes West", "Region", player)), combine="or")
                        add_rule(multiworld.get_location(("HP "+str(maxlv)), player),
                                 lambda state: (state.can_reach("Dunes West", "Region", player)), combine="or")
                        if maxlv == 5 or maxlv == 9 or maxlv == 13 or maxlv == 17:
                            add_rule(multiworld.get_location(("DEF "+str(maxlv)), player),
                                     lambda state: (state.can_reach("Dunes West", "Region", player)), combine="or")
                    elif curarea == "Dunes East":
                        add_rule(multiworld.get_location(("ATK "+str(maxlv)), player),
                                 lambda state: (state.can_reach("Dunes East", "Region", player)), combine="or")
                        add_rule(multiworld.get_location(("HP "+str(maxlv)), player),
                                 lambda state: (state.can_reach("Dunes East", "Region", player)), combine="or")
                        if maxlv == 5 or maxlv == 9 or maxlv == 13 or maxlv == 17:
                            add_rule(multiworld.get_location(("DEF "+str(maxlv)), player),
                                     lambda state: (state.can_reach("Dunes East", "Region", player)), combine="or")
                    elif curarea == "Wild East":
                        if _undertale_is_stats_rando(world, rando_stats=True):
                            add_rule(multiworld.get_location(("ATK "+str(maxlv)), player),
                                    lambda state: (state.can_reach("Wild East", "Region", player) and state.has("ATK Up", player, 9) and state.has("HP Up", player, 9)), combine="or")
                            add_rule(multiworld.get_location(("HP "+str(maxlv)), player),
                                    lambda state: (state.can_reach("Wild East", "Region", player) and state.has("ATK Up", player, 9) and state.has("HP Up", player, 9)), combine="or")
                            if maxlv == 5 or maxlv == 9 or maxlv == 13 or maxlv == 17:
                                add_rule(multiworld.get_location(("DEF "+str(maxlv)), player),
                                        lambda state: (state.can_reach("Wild East", "Region", player) and state.has("ATK Up", player, 9) and state.has("HP Up", player, 9)), combine="or")
                        elif _undertale_is_stats_rando(world, rando_stats=False) and _undertale_is_love_rando(world, rando_love=True):
                            add_rule(multiworld.get_location(("ATK "+str(maxlv)), player),
                                    lambda state: (state.can_reach("Wild East", "Region", player) and state.has("LOVE", player, 9)), combine="or")
                            add_rule(multiworld.get_location(("HP "+str(maxlv)), player),
                                    lambda state: (state.can_reach("Wild East", "Region", player) and state.has("LOVE", player, 9)), combine="or")
                            if maxlv == 5 or maxlv == 9 or maxlv == 13 or maxlv == 17:
                                add_rule(multiworld.get_location(("DEF "+str(maxlv)), player),
                                        lambda state: (state.can_reach("Wild East", "Region", player) and state.has("LOVE", player, 9)), combine="or")
                        else:
                            add_rule(multiworld.get_location(("ATK "+str(maxlv)), player),
                                    lambda state: (state.can_reach("Wild East", "Region", player)), combine="or")
                            add_rule(multiworld.get_location(("HP "+str(maxlv)), player),
                                    lambda state: (state.can_reach("Wild East", "Region", player)), combine="or")
                            if maxlv == 5 or maxlv == 9 or maxlv == 13 or maxlv == 17:
                                add_rule(multiworld.get_location(("DEF "+str(maxlv)), player),
                                        lambda state: (state.can_reach("Wild East", "Region", player)), combine="or")
                    elif curarea == "Steamworks Neutral":
                        if _undertale_is_stats_rando(world, rando_stats=True):
                            add_rule(multiworld.get_location(("ATK "+str(maxlv)), player),
                                    lambda state: (state.can_reach("Steamworks Neutral", "Region", player) and state.has("HP Up", player, 11) and state.has("Hydrochloric Acid", player)), combine="or")
                            add_rule(multiworld.get_location(("HP "+str(maxlv)), player),
                                    lambda state: (state.can_reach("Steamworks Neutral", "Region", player) and state.has("HP Up", player, 11) and state.has("Hydrochloric Acid", player)), combine="or")
                            if maxlv == 5 or maxlv == 9 or maxlv == 13 or maxlv == 17:
                                add_rule(multiworld.get_location(("DEF "+str(maxlv)), player),
                                        lambda state: (state.can_reach("Steamworks Neutral", "Region", player) and state.has("HP Up", player, 11) and state.has("Hydrochloric Acid", player)), combine="or")
                        elif _undertale_is_stats_rando(world, rando_stats=False) and _undertale_is_love_rando(world, rando_love=True):
                            add_rule(multiworld.get_location(("ATK "+str(maxlv)), player),
                                    lambda state: (state.can_reach("Steamworks Neutral", "Region", player) and state.has("LOVE", player, 11) and state.has("Hydrochloric Acid", player)), combine="or")
                            add_rule(multiworld.get_location(("HP "+str(maxlv)), player),
                                    lambda state: (state.can_reach("Steamworks Neutral", "Region", player) and state.has("LOVE", player, 11) and state.has("Hydrochloric Acid", player)), combine="or")
                            if maxlv == 5 or maxlv == 9 or maxlv == 13 or maxlv == 17:
                                add_rule(multiworld.get_location(("DEF "+str(maxlv)), player),
                                        lambda state: (state.can_reach("Steamworks Neutral", "Region", player) and state.has("LOVE", player, 11) and state.has("Hydrochloric Acid", player)), combine="or")
                        else:
                            add_rule(multiworld.get_location(("ATK "+str(maxlv)), player),
                                    lambda state: (state.can_reach("Steamworks Neutral", "Region", player) and state.has("Hydrochloric Acid", player) and state.has("Dunes Key", player)), combine="or")
                            add_rule(multiworld.get_location(("HP "+str(maxlv)), player),
                                    lambda state: (state.can_reach("Steamworks Neutral", "Region", player) and state.has("Hydrochloric Acid", player) and state.has("Dunes Key", player)), combine="or")
                            if maxlv == 5 or maxlv == 9 or maxlv == 13 or maxlv == 17:
                                add_rule(multiworld.get_location(("DEF "+str(maxlv)), player),
                                        lambda state: (state.can_reach("Steamworks Neutral", "Region", player) and state.has("Hydrochloric Acid", player) and state.has("Dunes Key", player)), combine="or")
                    elif curarea == "New Home":
                        if _undertale_is_stats_rando(world, rando_stats=True):
                            add_rule(multiworld.get_location(("ATK "+str(maxlv)), player),
                                    lambda state: (state.can_reach("New Home", "Region", player) and state.has("ATK Up", player, 18) and state.has("HP Up", player, 18)), combine="or")
                            add_rule(multiworld.get_location(("HP "+str(maxlv)), player),
                                    lambda state: (state.can_reach("New Home", "Region", player) and state.has("ATK Up", player, 18) and state.has("HP Up", player, 18)), combine="or")
                            if maxlv == 5 or maxlv == 9 or maxlv == 13 or maxlv == 17:
                                add_rule(multiworld.get_location(("DEF "+str(maxlv)), player),
                                        lambda state: (state.can_reach("New Home", "Region", player) and state.has("ATK Up", player, 18) and state.has("HP Up", player, 18)), combine="or")
                        elif _undertale_is_stats_rando(world, rando_stats=False) and _undertale_is_love_rando(world, rando_love=True):
                            add_rule(multiworld.get_location(("ATK "+str(maxlv)), player),
                                    lambda state: (state.can_reach("New Home", "Region", player) and state.has("LOVE", player, 18)), combine="or")
                            add_rule(multiworld.get_location(("HP "+str(maxlv)), player),
                                    lambda state: (state.can_reach("New Home", "Region", player) and state.has("LOVE", player, 18)), combine="or")
                            if maxlv == 5 or maxlv == 9 or maxlv == 13 or maxlv == 17:
                                add_rule(multiworld.get_location(("DEF "+str(maxlv)), player),
                                        lambda state: (state.can_reach("New Home", "Region", player) and state.has("LOVE", player, 18)), combine="or")
                        else:
                            add_rule(multiworld.get_location(("ATK "+str(maxlv)), player),
                                    lambda state: (state.can_reach("New Home", "Region", player)), combine="or")
                            add_rule(multiworld.get_location(("HP "+str(maxlv)), player),
                                    lambda state: (state.can_reach("New Home", "Region", player)), combine="or")
                            if maxlv == 5 or maxlv == 9 or maxlv == 13 or maxlv == 17:
                                add_rule(multiworld.get_location(("DEF "+str(maxlv)), player),
                                        lambda state: (state.can_reach("New Home", "Region", player)), combine="or")
                if world.options.rando_love:
                    if curarea == "Ruins":
                        add_rule(multiworld.get_location(("LOVE "+str(maxlv)), player),
                                 lambda state: (state.can_reach("Ruins", "Region", player)), combine="or")
                    elif curarea == "Snowdin":
                        add_rule(multiworld.get_location(("LOVE "+str(maxlv)), player),
                                 lambda state: (state.can_reach("Snowdin", "Region", player)), combine="or")
                    elif curarea == "Dunes West":
                        add_rule(multiworld.get_location(("LOVE "+str(maxlv)), player),
                                 lambda state: (state.can_reach("Dunes West", "Region", player)), combine="or")
                    elif curarea == "Dunes East":
                        add_rule(multiworld.get_location(("LOVE "+str(maxlv)), player),
                                 lambda state: (state.can_reach("Dunes East", "Region", player)), combine="or")
                    elif curarea == "Wild East":
                        if _undertale_is_stats_rando(world, rando_stats=True):
                            add_rule(multiworld.get_location(("LOVE "+str(maxlv)), player),
                                    lambda state: (state.can_reach("Wild East", "Region", player) and state.has("ATK Up", player, 9) and state.has("HP Up", player, 9)), combine="or")
                        elif _undertale_is_stats_rando(world, rando_stats=False) and _undertale_is_love_rando(world, rando_love=True):
                            add_rule(multiworld.get_location(("LOVE "+str(maxlv)), player),
                                    lambda state: (state.can_reach("Wild East", "Region", player) and state.has("LOVE", player, 9)), combine="or")
                        else:
                            add_rule(multiworld.get_location(("LOVE "+str(maxlv)), player),
                                    lambda state: (state.can_reach("Wild East", "Region", player)), combine="or")
                    elif curarea == "Steamworks Neutral":
                        if _undertale_is_stats_rando(world, rando_stats=True):
                            add_rule(multiworld.get_location(("LOVE "+str(maxlv)), player),
                                    lambda state: (state.can_reach("Steamworks Neutral", "Region", player) and state.has("HP Up", player, 11) and state.has("Hydrochloric Acid", player)), combine="or")
                        elif _undertale_is_stats_rando(world, rando_stats=False) and _undertale_is_love_rando(world, rando_love=True):
                            add_rule(multiworld.get_location(("LOVE "+str(maxlv)), player),
                                    lambda state: (state.can_reach("Steamworks Neutral", "Region", player) and state.has("LOVE", player, 11 and state.has("Hydrochloric Acid", player))), combine="or")
                        else:
                            add_rule(multiworld.get_location(("LOVE "+str(maxlv)), player),
                                    lambda state: (state.can_reach("Steamworks Neutral", "Region", player) and state.has("Hydrochloric Acid", player) and state.has("Dunes Key", player)), combine="or")
                    elif curarea == "New Home":
                        if _undertale_is_stats_rando(world, rando_stats=True):
                            add_rule(multiworld.get_location(("LOVE "+str(maxlv)), player),
                                    lambda state: (state.can_reach("New Home", "Region", player) and state.has("ATK Up", player, 18) and state.has("HP Up", player, 18) and state.has("ITEM", player)), combine="or")
                        elif _undertale_is_stats_rando(world, rando_stats=False) and _undertale_is_love_rando(world, rando_love=True):
                            add_rule(multiworld.get_location(("LOVE "+str(maxlv)), player),
                                    lambda state: (state.can_reach("New Home", "Region", player) and state.has("LOVE", player, 18) and state.has("ITEM", player)), combine="or")
                        else:
                            add_rule(multiworld.get_location(("LOVE "+str(maxlv)), player),
                                    lambda state: (state.can_reach("New Home", "Region", player) and state.has("ITEM", player)), combine="or")
            if curarea == "Ruins":
                curarea = "Snowdin"
                maxlv = 1
                exp = 180
            elif curarea == "Snowdin":
                curarea = "Dunes West"
                maxlv = 1
                exp = 920
            elif curarea == "Dunes West":
                curarea = "Dunes East"
                maxlv = 1
                exp = 80
            elif curarea == "Dunes East":
                curarea = "Wild East"
                maxlv = 1
                exp = 1500
            elif curarea == "Wild East":
                curarea = "Steamworks Neutral"
                maxlv = 1
                exp = 50000
            elif curarea == "Steamworks Neutral":
                curarea = "New Home"
                maxlv = 1
                exp = 99999
# Sets rules on completion condition
def set_completion_rules(world: "UndertaleYellowWorld"):
    player = world.player
    multiworld = world.multiworld
    if _undertale_is_route(world, 1) and (not _undertale_is_route(world, 3)):
        multiworld.completion_condition[player] = lambda state: (state.can_reach("Ketsukane Manor", "Region", player)
                                                                 and state.can_reach("New Home", "Region", player))
    elif _undertale_is_route(world, 2) and (not _undertale_is_route(world, 3)):
        multiworld.completion_condition[player] = lambda state: state.can_reach("New Home", "Region", player)
    elif _undertale_is_route(world, 0) and (not _undertale_is_route(world, 3)):
        multiworld.completion_condition[player] = lambda state: state.can_reach("New Home", "Region", player)
    elif _undertale_is_route(world, 3):
        if _undertale_is_stats_rando(world, rando_stats=True):
            multiworld.completion_condition[player] = lambda state: state.can_reach("New Home", "Region", player) and state.has("HP Up", player, 18) and state.has("ATK Up", player, 18) and state.has("ITEM", player) and (state.can_reach("Ketsukane Manor", "Region", player))
        elif _undertale_is_stats_rando(world, rando_stats=False) and _undertale_is_love_rando(world, rando_love=True):
            multiworld.completion_condition[player] = lambda state: state.can_reach("New Home", "Region", player) and state.has("LOVE", player, 18) and (state.can_reach("Ketsukane Manor", "Region", player))
        else:
            multiworld.completion_condition[player] = lambda state: state.can_reach("New Home", "Region", player) and (state.can_reach("Ketsukane Manor", "Region", player))