import pygame
import json

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0,-1), (1,-1), (1,0), (1,1) , (0,1), (0,0)]
PHYSICS_TILES = {'wood'}


class Tilemap:
    def __init__(self, game, tilesize = 18):
        self.game = game
        self.tilesize = tilesize
        self.tilemap = {}
        self.offgrid_tiles = []


    def extract(self, id_pairs, keep = False):
        matches = []

        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())

                if not keep:
                    self.offgrid_tiles.remove(tile)

        for loc in self.tilemap:
            tile = self.tilemap[loc]

            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tilesize
                matches[-1]['pos'][1] *= self.tilesize


                if not keep:
                    del self.tilemap[loc]


        matches = sorted(matches, key = lambda d:d['variant'])
        return matches


