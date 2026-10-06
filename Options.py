from Options import Choice, Toggle, Range, PerGameCommonOptions
from dataclasses import dataclass

class RouteRequired(Choice):
    """Route needed to goal"""
    display_name = "Required Route"
    option_neutral = 1
    option_pacifist = 2
    option_genocide = 3
    option_all_routes = 4
    default = 1

class StartingArea(Choice):
    """Area you start with a key for."""
    display_name = "Starting Area"
    option_ruins = 0
    option_snowdin = 1
    option_dunes = 2
    option_steamworks = 3
    default = 0

class ProgressiveArmor(Toggle):
    """Makes the armor progressive."""
    display_name = "Progressive Armor"
    default = 0

class ProgressiveAmmo(Toggle):
    """Makes the ammo progressive."""
    display_name = "Progressive Ammo"
    default = 0

class RandomizeLove(Toggle):
    """Adds LOVE to the pool. Only matters if your goal includes Genocide route"""
    display_name = "Randomize LOVE"
    default = 0

class RandomizeStats(Toggle):
    """Makes each stat increase from LV a separate item. Only matters if your goal includes Genocide route
    Warning: This tends to spam chat with sending out checks."""
    display_name = "Randomize Stats"
    default = 0

class RandoBattleOptions(Toggle):
    """Turns the ITEM button in battle into an item you have to receive."""
    display_name = "Randomize Item Button"
    default = 0

class ReduceGrind(Toggle):
    """Halves the amount of basic enemies needed to defeat per area in Genocide. Basic Enemies will give double experience to compensate.
    Also halves checks for Sparesanity and Killsanity"""
    display_name = "Reduce Grind"
    default = 0
class ExtraHP(Range):
    """Adds in extra HP Up's equal to the number set (Only affects Genocide/All Routes if State Rando is enabled)"""
    display_name = "Extra HP"
    default = 0
    range_start = 0
    range_end = 10
class ExtraATK(Range):
    """Adds in extra ATK Up's equal to the number set (Only affects Genocide/All Routes if Stat Rando is enabled)"""
    display_name = "Extra ATK"
    default = 0
    range_start = 0
    range_end = 10
class ExtraLOVE(Range):
    """Adds in extra LOVE equal to the number set (Only affects Genocide/All Routes if LOVE Rando is enabled and Stat Rando is disabled)"""
    display_name = "Extra LOVE"
    default = 0
    range_start = 0
    range_end = 10
class Minigames(Toggle):
    """Adds in Minigame Checks, including checks every 250 points in Mew Mew Love Blaster, Gold and Silver Rank in Six Shooter (45s and 75s respectively),
     and simply beating both minigames."""
    display_name = "Enable Minigames"
    default = 0
class SpareSanity(Toggle):
    "Makes Sparing Enemies checks, 20 checks per area (Reduced to 10 if Reduced Grind is on)"
    display_name = "Sparesanity"
    default = 0
class KillSanity(Toggle):
    "Makes Killing Enemies checks, 20 checks per area (Reduced to 10 if Reduced Grind is on)"
    display_name = "Killsanity"
    default = 0
@dataclass
class UndertaleYellowOptions(PerGameCommonOptions):
    route_required:                           RouteRequired
    starting_area:                            StartingArea
    prog_armor:                               ProgressiveArmor
    prog_ammo:                                ProgressiveAmmo
    rando_love:                               RandomizeLove
    rando_stats:                              RandomizeStats
    rando_item_button:                        RandoBattleOptions
    reduce_grind:                             ReduceGrind
    extra_hp:                                 ExtraHP
    extra_atk:                                ExtraATK
    extra_love:                               ExtraLOVE
    minigames:                                Minigames
    sparesanity:                              SpareSanity
    killsanity:                               KillSanity