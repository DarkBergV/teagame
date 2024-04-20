import pygame
import json

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (0, 0)]
PHYSICS_TILES = {"wood"}


class Tilemap:
    def __init__(self, game, tilesize=18):
        self.game = game
        self.tilesize = tilesize
        self.tilemap = {}
        self.offgrid_tiles = []

    def extract(self, id_pairs, keep=False):
        matches = []

        for tile in self.offgrid_tiles.copy():
            if (tile["type"], tile["variant"]) in id_pairs:
                matches.append(tile.copy())

                if not keep:
                    self.offgrid_tiles.remove(tile)

        for loc in self.tilemap:
            tile = self.tilemap[loc]

            if (tile["type"], tile["variant"]) in id_pairs:
                matches.append(tile.copy())
                matches[-1]["pos"] = matches[-1]["pos"].copy()
                matches[-1]["pos"][0] *= self.tilesize
                matches[-1]["pos"][1] *= self.tilesize

                if not keep:
                    del self.tilemap[loc]

        matches = sorted(matches, key=lambda d: d["variant"])
        return matches

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tilesize), int(pos[1] // self.tilesize))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = (
                tile_loc(pos[0] - offset[0]) + ";" + str(tile_loc[1] - offset[1])
            )

            if check_loc in self.tilemap:
                tiles.append(check_loc)

        return tiles

    def save(self, path):
        f = open(path, "w")

        json.dump(
            {
                "tilemap": self.tilemap,
                "tilesize": self.tilesize,
                "offgrid": self.offgrid_tiles,
            },
            f,
        )

        f.close()

    def load(self, path):

        f = open(path, "r")
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data["tilemap"]
        self.tilesize = map_data["tilesize"]
        self.offgrid_tiles = map_data["offgrid"]

    def physics_rect_around(self, pos):
        rects = []

        for tile in self.tiles_around(pos):
            if tile["type"] in PHYSICS_TILES:
                rects.append(
                    pygame.Rect(
                        tile[0] * self.tilesize,
                        tile[1] * self.tilesize,
                        self.tilesize,
                        self.tilesize,
                    )
                )

    def solid_check(self, pos):
        tile_loc = (int(pos[0] // self.tilesize), int(pos[1] // self.tilesize))

        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]["type"] in PHYSICS_TILES:
                return self.tilemap[tile_loc]

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(
                self.game.assets[tile["type"][tile["variant"]][tile["pos"]]],
                (tile["pos"][0] - offset[0], tile["pos"][1] - offset[1]),
            )

        for loc in self.tilemap:
            tile = self.tilemap[loc]

            surf.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                (
                    tile["pos"][0] * self.tilesize - offset[0],
                    tile["pos"][1] * self.tilesize - offset[1],
                ),
            )
