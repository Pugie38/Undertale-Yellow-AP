from BaseClasses import MultiWorld


def link_undertale_yellow_areas(world: MultiWorld, player: int):
    for (exit, region) in mandatory_connections:
        world.get_entrance(exit, player).connect(world.get_region(region, player))

undertale_yellow_regions = [
    ("Menu", ["New Game", "??? Exit"]),
    ("???", []),
    ("Hub", ["Ruins Hub", "Snowdin Hub", "Dunes Hub", "Steamworks Hub", "Hotland Hub"]),
    ("Ruins", []),
    ("Snowdin", []),
    ("Dunes West", ["Dunes East Entrance"]),
    ("Dunes East", ["Ketsukane Manor Entrance", "Wild East Entrance"]),
    ("Wild East", []),
    ("Ketsukane Manor", []),
    ("Steamworks Entrance", ["Steamworks Pacifist Entrance", "Steamworks Neutral Entrance"]),
    ("Steamworks Pacifist", ["Steamworks Axis Pacifist Entrance"]),
    ("Steamworks Neutral", ["Steamworks Axis Neutral Entrance"]),
    ("Steamworks Axis", []),
    ("Hotland", ["New Home Entrance"]),
    ("New Home", []),
]

mandatory_connections = [
    ("??? Exit", "???"),
    ("New Game", "Hub"),
    ("Ruins Hub", "Ruins"),
    ("Snowdin Hub", "Snowdin"),
    ("Dunes Hub", "Dunes West"),
    ("Dunes East Entrance", "Dunes East"),
    ("Wild East Entrance", "Wild East"),
    ("Ketsukane Manor Entrance", "Ketsukane Manor"),
    ("Steamworks Hub", "Steamworks Entrance"),
    ("Steamworks Pacifist Entrance", "Steamworks Pacifist"),
    ("Steamworks Neutral Entrance", "Steamworks Neutral"),
    ("Steamworks Axis Pacifist Entrance", "Steamworks Axis"),
    ("Steamworks Axis Neutral Entrance", "Steamworks Axis"),
    ("Hotland Hub", "Hotland"),
    ("New Home Entrance", "New Home"),
]
