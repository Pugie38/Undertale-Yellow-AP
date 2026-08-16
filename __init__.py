from .Items import UndertaleYellowItem, item_table, armor, ammo, non_key_items, key_items, \
    junk_weights
from .Locations import UndertaleYellowAdvancement, advancement_table, exclusion_table
from .Regions import undertale_yellow_regions, link_undertale_yellow_areas
from .Rules import set_rules, set_completion_rules
from worlds.generic.Rules import exclusion_rules
from BaseClasses import Region, Entrance, Tutorial, Item
from .Options import UndertaleYellowOptions
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components
from multiprocessing import Process


def run_client():
    print('running undertale yellow client')
    from .UndertaleYellowClient import main  # still lazy import idk what im doing lol
    p = Process(target=main)
    p.start()


components.append(Component("Undertale Yellow Client", func=run_client))
# components.append(Component("Undertale Client", func=run_client))


def data_path(file_name: str):
    import pkgutil
    return pkgutil.get_data(__name__, "data/" + file_name)


class UndertaleYellowWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Undertale Yellow software on your computer. This guide covers "
        "single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Pugie"]
    )]


class UndertaleYellowWorld(World):
    """
    Undertale Yellow is a fangame based on Undertale where every choice you make matters. Join Clover on a trip throughout new parts
     of the underground, joined by many new characters. Of course, all the routes present in Undertale are also present here.
    """
    game = "Undertale Yellow"
    options_dataclass = UndertaleYellowOptions
    options: UndertaleYellowOptions
    web = UndertaleYellowWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in advancement_table.items()}

    def _get_undertale_yellow_data(self):
        return {
            "world_seed": self.random.getrandbits(32),
            "seed_name": self.multiworld.seed_name,
            "player_name": self.multiworld.get_player_name(self.player),
            "player_id": self.player,
            "client_version": self.required_client_version,
            "race": self.multiworld.is_race,
            "route": self.options.route_required.current_key,
            "starting_area": self.options.starting_area.current_key,
            "rando_love": bool(self.options.rando_love and (self.options.route_required == "genocide" or self.options.route_required == "all_routes")),
            "rando_stats": bool(self.options.rando_stats and (self.options.route_required == "genocide" or self.options.route_required == "all_routes")),
            "prog_armor": bool(self.options.prog_armor.value),
            "prog_ammo": bool(self.options.prog_ammo.value),
            "rando_item_button": bool(self.options.rando_item_button.value),
            "route_required": int(self.options.route_required.value),
            "reduce_grind": bool(self.options.reduce_grind.value),

        }

    def get_filler_item_name(self):
        junk_pool = junk_weights
        return self.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()))[0]

    def create_items(self):
        # Generate item pool
        itempool = []
        # Add all required progression items
        for name, num in key_items.items():
            itempool += [name] * num
        for name, num in armor.items():
            itempool += [name] * num
        for name, num in ammo.items():
            itempool += [name] * num
        for name, num in non_key_items.items():
            itempool += [name] * num
        if self.options.rando_item_button:
            itempool += ["ITEM"]
        else:
            self.multiworld.push_precollected(self.create_item("ITEM"))
        if self.options.route_required == "genocide":
            itempool = [item for item in itempool if item != "Broken Amulet" and item != "Cake" and item != "Nice Hat" and item != "Soggy Mitten" and item != "Snowdin Map" and item != "Matches" and item != "Lukewarm Coffee"]
        elif self.options.route_required == "pacifist":
            itempool = [item for item in itempool if item != "Hydrochloric Acid"]
        if not self.options.rando_love or \
                (self.options.route_required != "genocide" and self.options.route_required != "all_routes"):
            itempool = [item for item in itempool if not item == "LOVE"]
        if not self.options.rando_stats or \
                (self.options.route_required != "genocide" and self.options.route_required != "all_routes"):
            itempool = [item for item in itempool if not (item == "ATK Up" or item == "DEF Up" or item == "HP Up")]
        if self.options.prog_armor:
            itempool = [item if (item not in armor) else
                        "Progressive Armor" for item in itempool]
        if self.options.prog_ammo:
            itempool = [item if item not in ammo else "Progressive Ammo" for item in itempool]
        if self.options.extra_stats:
                if self.options.route_required == "genocide" or self.options.route_required == "all_routes":
                    if self.options.rando_stats:
                            itempool += ["ATK Up"] * 10
                            itempool += ["HP Up"] * 10
                    elif self.options.rando_love:
                            itempool += ["LOVE"] * 10

        starting_key = self.options.starting_area.current_key.title() + " Key"
        itempool.remove(starting_key)
        self.multiworld.push_precollected(self.create_item(starting_key))
        # Choose locations to automatically exclude based on settings
        exclusion_pool = set()
        exclusion_pool.update(exclusion_table[self.options.route_required.current_key])
        if not self.options.rando_love or \
                (self.options.route_required != "genocide" and self.options.route_required != "all_routes"):
            exclusion_pool.update(exclusion_table["NoLove"])
        if not self.options.rando_stats or \
                (self.options.route_required != "genocide" and self.options.route_required != "all_routes"):
            exclusion_pool.update(exclusion_table["NoStats"])
        if not self.options.minigames:
            exclusion_pool.update(exclusion_table["NoMinigames"])

        # Choose locations to automatically exclude based on settings
        exclusion_checks = set()
        exclusion_checks.update([])
        exclusion_rules(self.multiworld, self.player, exclusion_checks)

        # Convert itempool into real items
        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]
        # Fill remaining items with randomly generated junk
        while len(itempool) < len(self.multiworld.get_unfilled_locations(self.player)):
            itempool.append(self.create_filler())

        self.multiworld.itempool += itempool

    def set_rules(self):
        set_rules(self)
        set_completion_rules(self)

    def create_regions(self):
        def UndertaleYellowRegion(region_name: str, exits=[]):
            ret = Region(region_name, self.player, self.multiworld)
            ret.locations += [UndertaleYellowAdvancement(self.player, loc_name, loc_data.id, ret)
                              for loc_name, loc_data in advancement_table.items()
                              if loc_data.region == region_name and
                              (loc_name not in exclusion_table["NoMinigames"] or
                               (self.options.minigames and self.options.route_required != "genocide")) and
                              (loc_name not in exclusion_table["NoStats"] or
                              (self.options.rando_stats and
                               (self.options.route_required == "genocide" or
                                self.options.route_required == "all_routes"))) and
                              (loc_name not in exclusion_table["NoLove"] or
                              (self.options.rando_love and
                               (self.options.route_required == "genocide" or
                                self.options.route_required == "all_routes"))) and
                              loc_name not in exclusion_table[self.options.route_required.current_key]]
            for exit in exits:
                ret.exits.append(Entrance(self.player, exit, ret))
            return ret

        self.multiworld.regions += [UndertaleYellowRegion(*r) for r in undertale_yellow_regions]
        link_undertale_yellow_areas(self.multiworld, self.player)

    def fill_slot_data(self):
        return self._get_undertale_yellow_data()

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = UndertaleYellowItem(name, item_data.classification, item_data.code, self.player)
        return item
