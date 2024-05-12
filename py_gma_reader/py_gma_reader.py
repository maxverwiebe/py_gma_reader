import os
import json
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
import struct

ADDON_IDENT = "GMAD"
ADDON_VERSION = 3

class AddonType(Enum):
    GAMEMODE = "gamemode"
    MAP = "map"
    WEAPON = "weapon"
    VEHICLE = "vehicle"
    NPC = "npc"
    ENTITY = "entity"
    TOOL = "tool"
    EFFECTS = "effects"
    MODEL = "model"
    SERVER_CONTENT = "servercontent"

class AddonTag(Enum):
    FUN = "fun"
    ROLEPLAY = "roleplay"
    SCENIC = "scenic"
    MOVIE = "movie"
    REALISM = "realism"
    CARTOON = "cartoon"
    WATER = "water"
    COMIC = "comic"
    BUILD = "build"

class AddonFile:
    def __init__(self, file_id, name, size, crc, offset):
        self.file_id = file_id
        self.name = name
        self.size = size
        self.crc = crc
        self.offset = offset

class GModAddon:
    def __init__(self):
        self.source = None
        self.file_block_offset = 0
        self.format_version = 0
        self.steam_id = 0
        self.timestamp = 0
        self.required_content = ""
        self.name = ""
        self.description = ""
        self.addon_type = ""
        self.tags = []
        self.author = ""
        self.version = 0
        self.files = []
        
    def __repr__(self):
        return f"GModAddon(name={self.name}, author={self.author}, type={self.addon_type}, tags={self.tags}, version={self.version}, file_count={len(self.files)})"

    def extract_files(self, destination):
        os.makedirs(destination, exist_ok=True)

        def extract_single_file(file_entry):
            file_path = os.path.join(destination, file_entry.name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            offset = self.file_block_offset + file_entry.offset
            self.source.seek(offset)
            data = self.source.read(file_entry.size)
            with open(file_path, "wb") as file:
                file.write(data)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(extract_single_file, file_entry) for file_entry in self.files]
            for future in futures:
                future.result()

class AddonReader:
    def __init__(self, source):
        self.source = source

    def read_byte(self):
        return self.source.read(1)[0]

    def read_bytes(self, count):
        return self.source.read(count)

    def read_uint32(self):
        return struct.unpack("<I", self.read_bytes(4))[0]

    def read_uint64(self):
        return struct.unpack("<Q", self.read_bytes(8))[0]

    def read_int32(self):
        return struct.unpack("<i", self.read_bytes(4))[0]

    def read_string(self):
        bstring = bytearray(b'')
        while True:
            char = self.source.read(1)
            if not char or char == b"\0":
                break
            bstring.extend(char)
        return bstring.decode()

    def parse_addon(self):
        addon = GModAddon()

        self.source.seek(0)

        ident = self.read_bytes(4).decode()
        if ident != ADDON_IDENT:
            raise ValueError("Invalid GMA file")

        addon.format_version = self.read_byte()
        if addon.format_version > ADDON_VERSION:
            raise ValueError("Unsupported addon version")

        addon.steam_id = self.read_uint64()
        addon.timestamp = self.read_uint64()

        if addon.format_version > 1:
            while True:
                content = self.read_string()
                if not content:
                    break
                addon.required_content += content

        addon.name = self.read_string()
        addon.description = self.read_string()

        try:
            parsed_description = json.loads(addon.description)
            addon.description = parsed_description.get("description", "")
            addon.addon_type = AddonType(parsed_description.get("type", ""))
            addon.tags = [AddonTag(tag) for tag in parsed_description.get("tags", [])]
        except json.JSONDecodeError:
            pass

        addon.author = self.read_string()
        addon.version = self.read_int32()

        offset = 0
        while True:
            file_id = self.read_uint32()
            if file_id == 0:
                break
            file_name = self.read_string()
            file_size = self.read_uint64()
            file_crc = self.read_uint32()
            file_entry = AddonFile(file_id, file_name, file_size, file_crc, offset)
            offset += file_size
            addon.files.append(file_entry)

        addon.source = self.source
        addon.file_block_offset = self.source.tell()

        return addon