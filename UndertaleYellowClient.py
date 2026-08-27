from __future__ import annotations
import os
import asyncio
import typing
import bsdiff4
import Utils

from NetUtils import NetworkItem, ClientStatus
from worlds import undertale_yellow
from MultiServer import mark_raw
from CommonClient import CommonContext, server_loop, \
    gui_enabled, ClientCommandProcessor, logger, get_base_parser
from Utils import async_start


class UndertaleYellowCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    def _cmd_resync(self):
        """Manually trigger a resync."""
        if isinstance(self.ctx, UndertaleYellowContext):
            self.output(f"Syncing items.")
            self.ctx.syncing = True

    def _cmd_patch(self):
        """Patch the game."""
        if isinstance(self.ctx, UndertaleYellowContext):
            os.makedirs(name=Utils.user_path("Undertale Yellow v-1-3-1"), exist_ok=True)
            self.ctx.patch_game()
            self.output("Patched.")

    def _cmd_savepath(self, directory: str):
        """Redirect to proper save data folder. This is necessary for Linux users to use before connecting."""
        if isinstance(self.ctx, UndertaleYellowContext):
            self.ctx.save_game_folder = directory
            self.output("Changed to the following directory: " + self.ctx.save_game_folder)

    @mark_raw

    def _cmd_deathlink(self):
        """Toggles deathlink"""
        if isinstance(self.ctx, UndertaleYellowContext):
            self.ctx.deathlink_status = not self.ctx.deathlink_status
            if self.ctx.deathlink_status:
                self.output(f"Deathlink enabled.")
            else:
                self.output(f"Deathlink disabled.")


class UndertaleYellowContext(CommonContext):
    tags = {"AP", "Online"}
    game = "Undertale"
    command_processor = UndertaleYellowCommandProcessor
    items_handling = 0b111
    route = None
    completed_routes = None
    completed_count = 0
    save_game_folder = os.path.expandvars(r"%localappdata%/Undertale_Yellow")

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.finished_game = False
        self.game = "Undertale Yellow"
        self.got_deathlink = False
        self.syncing = False
        self.deathlink_status = False
        self.tem_armor = False
        self.completed_count = 0
        self.completed_routes = {"pacifist": 0, "genocide": 0, "neutral": 0}
        # self.save_game_folder: files go in this path to pass data between us and the actual game
        self.save_game_folder = os.path.expandvars(r"%localappdata%/Undertale_Yellow")

    def patch_game(self):
        with open(Utils.user_path("Undertale Yellow v-1-3-1", "data.win"), "rb") as f:
            patchedFile = bsdiff4.patch(f.read(), undertale_yellow.data_path("Patch.bsdiff"))
        with open(Utils.user_path("Undertale Yellow v-1-3-1", "data.win"), "wb") as f:
            f.write(patchedFile)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def clear_undertale_yellow_files(self):
        path = self.save_game_folder
        self.finished_game = False
        for root, dirs, files in os.walk(path):
            for file in files:
                if "check.spot" == file or "scout" == file:
                    os.remove(os.path.join(root, file))
                elif file.endswith((".item", ".victory", ".route", ".playerspot", ".mad",
                                            ".youDied", ".LV", ".mine", ".flag", ".hint", ".grind")):
                    os.remove(os.path.join(root, file))

    async def connect(self, address: typing.Optional[str] = None):
        self.clear_undertale_yellow_files()
        await super().connect(address)

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.clear_undertale_yellow_files()
        await super().disconnect(allow_autoreconnect)

    async def connection_closed(self):
        self.clear_undertale_yellow_files()
        await super().connection_closed()

    async def shutdown(self):
        self.clear_undertale_yellow_files()
        await super().shutdown()

    def update_online_mode(self, online):
        old_tags = self.tags.copy()
        if online:
            self.tags.add("Online")
        else:
            self.tags -= {"Online"}
        if old_tags != self.tags and self.server and not self.server.socket.closed:
            async_start(self.send_msgs([{"cmd": "ConnectUpdate", "tags": self.tags}]))

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game
        async_start(process_undertale_yellow_cmd(self, cmd, args))

    def run_gui(self):
        from kvui import GameManager

        class UTManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Undertale Yellow Client"

        self.ui = UTManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_deathlink(self, data: typing.Dict[str, typing.Any]):
        self.got_deathlink = True
        super().on_deathlink(data)


def to_room_name(place_name: str):
    if place_name == "Old Home Exit":
        return "room_ruinsexit"
    elif place_name == "Snowdin Forest":
        return "room_tundra1"
    elif place_name == "Snowdin Town Exit":
        return "room_fogroom"
    elif place_name == "Waterfall":
        return "room_water1"
    elif place_name == "Waterfall Exit":
        return "room_fire2"
    elif place_name == "Hotland":
        return "room_fire_prelab"
    elif place_name == "Hotland Exit":
        return "room_fire_precore"
    elif place_name == "Core":
        return "room_fire_core1"


async def process_undertale_yellow_cmd(ctx: UndertaleYellowContext, cmd: str, args: dict):
    if cmd == "Connected":
        if not os.path.exists(ctx.save_game_folder):
            os.mkdir(ctx.save_game_folder)
        ctx.route = args["slot_data"]["route"]


        await ctx.send_msgs([{"cmd": "Get", "keys": [str(ctx.slot)+" RoutesDone neutral",
                                                     str(ctx.slot)+" RoutesDone pacifist",
                                                     str(ctx.slot)+" RoutesDone genocide"]}])
        await ctx.send_msgs([{"cmd": "SetNotify", "keys": [str(ctx.slot)+" RoutesDone neutral",
                                                           str(ctx.slot)+" RoutesDone pacifist",
                                                           str(ctx.slot)+" RoutesDone genocide"]}])
        if args["slot_data"]["rando_love"]:
            filename = f"LOVErando.LV"
            with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
                f.close()
        if args["slot_data"]["rando_stats"]:
            filename = f"STATrando.LV"
            with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
                f.close()
        if args["slot_data"]["reduce_grind"]:
            filename = f"reducegrind.grind"
            with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
                f.close()
        filename = f"{ctx.route}.route"
        with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
            f.close()
        filename = f"check.spot"
        with open(os.path.join(ctx.save_game_folder, filename), "a") as f:
            for ss in set(args["checked_locations"]):
                f.write(str(ss-12000)+"\n")
            f.close()
    elif cmd == "LocationInfo":
        for l in args["locations"]:
            locationid = l.location
            filename = f"{str(locationid-12000)}.hint"
            with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
                toDraw = ""
                for i in range(20):
                    if i < len(str(ctx.item_names.lookup_in_game(l.item))):
                        toDraw += str(ctx.item_names.lookup_in_game(l.item))[i]
                    else:
                        break
                f.write(toDraw)
                f.close()
    elif cmd == "Retrieved":
        if str(ctx.slot)+" RoutesDone neutral" in args["keys"]:
            if args["keys"][str(ctx.slot)+" RoutesDone neutral"] is not None:
                ctx.completed_routes["neutral"] = args["keys"][str(ctx.slot)+" RoutesDone neutral"]
        if str(ctx.slot)+" RoutesDone genocide" in args["keys"]:
            if args["keys"][str(ctx.slot)+" RoutesDone genocide"] is not None:
                ctx.completed_routes["genocide"] = args["keys"][str(ctx.slot)+" RoutesDone genocide"]
        if str(ctx.slot)+" RoutesDone pacifist" in args["keys"]:
            if args["keys"][str(ctx.slot) + " RoutesDone pacifist"] is not None:
                ctx.completed_routes["pacifist"] = args["keys"][str(ctx.slot)+" RoutesDone pacifist"]
    elif cmd == "SetReply":
        if args["value"] is not None:
            if str(ctx.slot)+" RoutesDone pacifist" == args["key"]:
                ctx.completed_routes["pacifist"] = args["value"]
            elif str(ctx.slot)+" RoutesDone genocide" == args["key"]:
                ctx.completed_routes["genocide"] = args["value"]
            elif str(ctx.slot)+" RoutesDone neutral" == args["key"]:
                ctx.completed_routes["neutral"] = args["value"]
    elif cmd == "ReceivedItems":
        start_index = args["index"]

        if start_index == 0:
            ctx.items_received = []
        elif start_index != len(ctx.items_received):
            sync_msg = [{"cmd": "Sync"}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks",
                                 "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
        if start_index == len(ctx.items_received):
            counter = -1
            placedAmmo = 0
            placedArmor = 0
            for item in args["items"]:
                id = NetworkItem(*item).location
                while NetworkItem(*item).location < 0 and \
                        counter <= id:
                    id -= 1
                if NetworkItem(*item).location < 0:
                    counter -= 1
                filename = f"{str(id)}PLR{str(NetworkItem(*item).player)}.item"
                with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
                    if NetworkItem(*item).item == 97508:
                        if placedAmmo == 0:
                            f.write(str(97520-11000))
                        elif placedAmmo == 1:
                            f.write(str(97521-11000))
                        elif placedAmmo == 2:
                            f.write(str(97522-11000))
                        elif placedAmmo == 3:
                            f.write(str(97523-11000))
                        elif placedAmmo == 4:
                            f.write(str(97524-11000))
                        elif placedAmmo == 5:
                            f.write(str(97525-11000))
                        elif placedAmmo == 6:
                            f.write(str(97526-11000))
                        elif placedAmmo == 7:
                            f.write(str(97527-11000))
                        else:
                            f.write(str(97579-11000))
                        placedAmmo += 1
                    elif NetworkItem(*item).item == 97507:
                        if placedArmor == 0:
                            f.write(str(97509-11000))
                        elif placedArmor == 1:
                            f.write(str(97510-11000))
                        elif placedArmor == 2:
                            f.write(str(97511-11000))
                        elif placedArmor == 3:
                            f.write(str(97513-11000))
                        elif placedArmor == 4:
                            f.write(str(97514-11000))
                        elif placedArmor == 5:
                            f.write(str(97515-11000))
                        elif placedArmor == 6:
                            f.write(str(97516-11000))
                        elif placedArmor == 7:
                            f.write(str(97517-11000))
                        elif placedArmor == 8:
                            f.write(str(97518-11000))
                        elif placedArmor == 9:
                            f.write(str(97519-11000))
                        else:
                            f.write(str(97580-11000))
                        placedArmor += 1
                    else:
                        f.write(str(NetworkItem(*item).item-11000))
                    f.close()
                ctx.items_received.append(NetworkItem(*item))
        ctx.watcher_event.set()

    elif cmd == "RoomUpdate":
        if "checked_locations" in args:
            filename = f"check.spot"
            with open(os.path.join(ctx.save_game_folder, filename), "a") as f:
                for ss in set(args["checked_locations"]):
                    f.write(str(ss-12000)+"\n")
                f.close()

    elif cmd == "Bounced":
        tags = args.get("tags", [])
        if "Online" in tags:
            data = args.get("data", {})
            if data["player"] != ctx.slot and data["player"] is not None:
                filename = f"FRISK" + str(data["player"]) + ".playerspot"
                with open(os.path.join(ctx.save_game_folder, filename), "w") as f:
                    f.write(str(data["x"]) + str(data["y"]) + str(data["room"]) + str(
                        data["spr"]) + str(data["frm"]))
                    f.close()


async def multi_watcher(ctx: UndertaleYellowContext):
    while not ctx.exit_event.is_set():
        path = ctx.save_game_folder
        for root, dirs, files in os.walk(path):
            for file in files:
                if "spots.mine" in file and "Online" in ctx.tags:
                    with open(os.path.join(root, file), "r") as mine:
                        this_x = mine.readline()
                        this_y = mine.readline()
                        this_room = mine.readline()
                        this_sprite = mine.readline()
                        this_frame = mine.readline()
                        mine.close()
                    message = [{"cmd": "Bounce", "tags": ["Online"],
                                "data": {"player": ctx.slot, "x": this_x, "y": this_y, "room": this_room,
                                         "spr": this_sprite, "frm": this_frame}}]
                    await ctx.send_msgs(message)

        await asyncio.sleep(0.1)


async def game_watcher(ctx: UndertaleYellowContext):
    while not ctx.exit_event.is_set():
        await ctx.update_death_link(ctx.deathlink_status)
        path = ctx.save_game_folder
        if ctx.syncing:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if ".item" in file:
                        os.remove(os.path.join(root, file))
            sync_msg = [{"cmd": "Sync"}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
        if ctx.got_deathlink:
            ctx.got_deathlink = False
            with open(os.path.join(ctx.save_game_folder, "WelcomeToTheDead.youDied"), "w") as f:
                f.close()
        sending = []
        victory = False
        found_routes = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                if "DontBeMad.mad" in file:
                    os.remove(os.path.join(root, file))
                    if "DeathLink" in ctx.tags:
                        await ctx.send_death()
                if "scout" == file:
                    sending = []
                    try:
                        with open(os.path.join(root, file), "r") as f:
                            lines = f.readlines()
                        for l in lines:
                            if ctx.server_locations.__contains__(int(l)+12000):
                                sending = sending + [int(l.rstrip('\n'))+12000]
                    finally:
                        await ctx.send_msgs([{"cmd": "LocationScouts", "locations": sending,
                                                          "create_as_hint": int(2)}])
                        os.remove(os.path.join(root, file))
                if "check.spot" in file:
                    sending = []
                    try:
                        with open(os.path.join(root, file), "r") as f:
                            lines = f.readlines()
                        for l in lines:
                            sending = sending+[(int(l.rstrip('\n')))+12000]
                    finally:
                        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": sending}])
                if "victory" in file and str(ctx.route) in file:
                    victory = True
                if ".playerspot" in file and "Online" not in ctx.tags:
                    os.remove(os.path.join(root, file))
                if "victory" in file:
                    if str(ctx.route) == "all_routes":
                        if "neutral" in file and ctx.completed_routes["neutral"] != 1:
                            await ctx.send_msgs([{"cmd": "Set", "key": str(ctx.slot)+" RoutesDone neutral",
                                                  "default": 0, "want_reply": True, "operations": [{"operation": "max",
                                                                                                    "value": 1}]}])
                        elif "pacifist" in file and ctx.completed_routes["pacifist"] != 1:
                            await ctx.send_msgs([{"cmd": "Set", "key": str(ctx.slot)+" RoutesDone pacifist",
                                                  "default": 0, "want_reply": True, "operations": [{"operation": "max",
                                                                                                    "value": 1}]}])
                        elif "genocide" in file and ctx.completed_routes["genocide"] != 1:
                            await ctx.send_msgs([{"cmd": "Set", "key": str(ctx.slot)+" RoutesDone genocide",
                                                  "default": 0, "want_reply": True, "operations": [{"operation": "max",
                                                                                                    "value": 1}]}])
        if str(ctx.route) == "all_routes":
            found_routes += ctx.completed_routes["neutral"]
            found_routes += ctx.completed_routes["pacifist"]
            found_routes += ctx.completed_routes["genocide"]
        if str(ctx.route) == "all_routes" and found_routes >= 3:
            victory = True
        ctx.locations_checked = sending
        if (not ctx.finished_game) and victory:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        await asyncio.sleep(0.1)


def main():
    Utils.init_logging("UndertaleYellowClient", exception_logger="Client")

    async def _main():
        ctx = UndertaleYellowContext(None, None)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        asyncio.create_task(
            game_watcher(ctx), name="UndertaleYellowProgressionWatcher")

        asyncio.create_task(
            multi_watcher(ctx), name="UndertaleYellowMultiplayerWatcher")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    colorama.just_fix_windows_console()

    asyncio.run(_main())
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser(description="Undertale Yellow Client, for text interfacing.")
    args = parser.parse_args()
    main()
