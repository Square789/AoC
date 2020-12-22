from aoc_input import get_input
import aoc_helpers as ah

from collections import namedtuple
import numpy as np
import re

np.set_printoptions(linewidth=200, threshold=10000)

PlacedTile = namedtuple("PlacedTile", ("tile", "cw_rot", "flip_after_rot", "sourceedge"))
Connection = namedtuple("Connection", ("tile", "edge", "flip_after_rot"))

RE_NUM = re.compile(r"\d+")

DAY = 20
YEAR = 2020

DIM = 10
CHOP_DIM = DIM - 2
CW_ROT = {"t": 0, "r": 1, "b": 2, "l": 3}
CW_ROTR = ("t", "r", "b", "l")
#    t r b l
# t] 2 1 0 3 (2 - x) % 4
# r] 3 2 1 0 (3 - x) % 4
# b] 0 3 2 1 (-x) % 4
# l] 1 0 3 2 (1 - x) % 4

MONSTER = np.array((
	(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,),
	(1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,1,),
	(0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,),
 ), dtype=np.uint8)

MONSTER_TRUTH_ARRAY = (MONSTER == 1)

class Tile():
	def __init__(self, data, id_):
		self.data = data
		self.id = id_

		top = self.data[0]
		rgt = "".join(self.data[i][DIM - 1] for i in range(DIM))
		btm = self.data[DIM - 1][::-1]
		lft = "".join(self.data[i][0] for i in reversed(range(DIM)))
		self.edges = {
			"t": tuple(hash(s) for s in (top, top[::-1])),
			"l": tuple(hash(s) for s in (lft, lft[::-1])),
			"r": tuple(hash(s) for s in (rgt, rgt[::-1])),
			"b": tuple(hash(s) for s in (btm, btm[::-1])),
		}

		self.connectable = {
			"t": None,
			"l": None,
			"r": None,
			"b": None,
		}

	def __repr__(self):
		return f"<Tile id={self.id}>"

	def find_connectable(self, tiles):
		for tile in tiles:
			if tile.id == self.id:
				continue
			for edge, (hash_, _) in self.edges.items():
				for otheredge, otherhashes in tile.edges.items():
					if hash_ in otherhashes:
						if self.connectable[edge] is not None:
							raise ValueError("Edge already has a connection candidate,"
								" and I am not writing code to resolve those conflicts.")
						self.connectable[edge] = Connection(
							tile, otheredge, hash_ == otherhashes[0])

	def clip_border(self):
		self.data.pop(-1)
		self.data.pop(0)
		for i, line in enumerate(self.data):
			self.data[i] = line[1:-1]


def sol0(tiles):
	for tile in tiles:
		tile.find_connectable(tiles)

	acc = 1
	for tile in tiles:
		if sum((con is not None) for con in tile.connectable.values()) == 2:
			acc *= tile.id

	return acc

def sol1(tiles):
	# Tiles will be preprocessed by sol0
	for tile in tiles:
		tile.clip_border()

	tilemap_dim = len(tiles)**.5

	if not tilemap_dim.is_integer():
		raise ValueError("Amount of tiles must be square of a whole number.")

	tilemap_dim = int(tilemap_dim)

	tilemap = [[None]*tilemap_dim for _ in range(tilemap_dim)]

	# Locate a corner tile
	for tile in tiles:
		if sum((con is not None) for con in tile.connectable.values()) == 2:
			break

	# Variables responsible for looping direction
	# X/Y position, X/Y direction, X reset, Adjacent tile's common edge
	if tile.connectable["l"]:
		x = tilemap_dim - 2
		xd = -1
		xr = tilemap_dim - 1
		sx = "l"
	else:
		x = 1 #
		xd = 1
		xr = 0
		sx = "r"

	if tile.connectable["t"]:
		y = tilemap_dim - 1 #
		yd = -1
		sy = "t"
	else:
		y = 0
		yd = 1
		sy = "b"

	# Corner tile effectively serves as the origin of all other tiles
	# t[0]: tile reference, t[1]: rotations clockwise, t[2]: whether to flip
	# after rotating, t[3]: grid relative direction the tile originated from
	# ( Loop starts with the field after the first field, gotta subtract here)
	tilemap[y][x - xd] = PlacedTile(tile, 0, False, None)

	# Fill in tiles
	while 0 <= y < tilemap_dim:
		while 0 <= x < tilemap_dim:
			if x == xr: # Use tile adjacent y-wise, since this line is empty
				sourcetile = tilemap[y - yd][x]
				sourceedge = sy
			else: # Use previous tile
				sourcetile = tilemap[y][x - xd]
				sourceedge = sx

			# print(f"({x},{y}) would be fed from " +
			#	(f"({x},{y-yd})" if x == xr else f"({x-xd},{y}). ") + f"{sourcetile.tile}")

			adjusted_source_edge = CW_ROTR[(CW_ROT[sourceedge] - sourcetile.cw_rot) % 4]
			# If the corner tile was flipped, it will for example face the bottom side to
			# the current field instead of the top one:
			#  |   |               | f |
			#  b > t               t < b
			#  |   |               |   |
			#  \-r-/               \-r-/
			#  ----- flip upper -> -----
			#  /-t-\               /-t-\
			#  |   |               |   |
			#  l ^ r               l ^ r
			#  |   |               |   |
			if x == xr + xd and sourcetile.flip_after_rot:
				adjusted_source_edge = CW_ROTR[(CW_ROT[adjusted_source_edge] + 2) % 4]

			# print(f"The edge of the source tile seen from its original orientation touching "
			#	f"this slot is {adjusted_source_edge}.")
			# print(f"Previous tile: {sourcetile.tile}, {sourcetile.tile.connectable}")
			# print(f"-> This slot will be occupied using " +
			#	f"{sourcetile.tile.connectable[adjusted_source_edge]}")

			newtile_conn = sourcetile.tile.connectable[adjusted_source_edge]
			newtile_rots = (((CW_ROT[sourceedge] + 2) % 4) - CW_ROT[newtile_conn.edge]) % 4
			newtile_flippage = sourcetile.flip_after_rot ^ newtile_conn.flip_after_rot

			# print(f"Newly placed tile's connected edge to the source tile is " +
			#	f"{newtile_conn.edge} and will need to be rotated clockwise {newtile_rots} times.")
			# print(f"Source tile is {'not '*(1^sourcetile.flip_after_rot)}flipped, so the new "
			#	f"tile will f"{'not '*(1^newtile_flippage)}be flipped overall.")

			tilemap[y][x] = PlacedTile(
				newtile_conn.tile,
				newtile_rots,
				newtile_flippage,
				sourceedge
			)

			x += xd
		y += yd
		x = xr

	# Concat tiles into numpy array
	arr_dim = tilemap_dim * CHOP_DIM
	array = np.zeros((arr_dim, arr_dim), dtype=np.uint8)
	for y in range(tilemap_dim):
		for x in range(tilemap_dim):
			tilearray = np.zeros((CHOP_DIM, CHOP_DIM), dtype=np.uint8)
			tiletup = tilemap[y][x]
			for suby in range(CHOP_DIM):
				for subx in range(CHOP_DIM):
					tilearray[suby, subx] = int(tiletup.tile.data[suby][subx] == "#")
			tilearray = np.rot90(tilearray, (4 - tilemap[y][x].cw_rot) % 4)
			if tiletup.flip_after_rot and CW_ROT[tiletup.sourceedge] & 1: # Up/Down
				tilearray = np.flipud(tilearray)
			elif tiletup.flip_after_rot and not CW_ROT[tiletup.sourceedge] & 1: # Left/Right
				tilearray = np.fliplr(tilearray)
			array[CHOP_DIM*y:CHOP_DIM*(y+1), CHOP_DIM*x:CHOP_DIM*(x+1)] = tilearray

	# Find monster by going ham on the array and guessing the correct orientation
	monster_found = False
	for i in range(6):
		for y in range(arr_dim - MONSTER.shape[0]):
			for x in range(arr_dim - MONSTER.shape[1]):
				if ((array[y:y + MONSTER.shape[0], x:x + MONSTER.shape[1]] + MONSTER == 2) \
					== MONSTER_TRUTH_ARRAY
				).all():
					monster_found = True
					array[y:y + MONSTER.shape[0], x:x + MONSTER.shape[1]] -= MONSTER
		if monster_found:
			break
		array = np.rot90(array)
		if i == 4:
			array = np.flipud(array)

	# Return and never look at this puzzle again
	return (array == 1).sum()

def main():
	puzzle_in = [
		block.split("\n")
		for block in get_input(YEAR, DAY).strip().split("\n\n")
	]

	tiles = [
		Tile(block[1:], int(RE_NUM.search(block[0])[0]))
		for block in puzzle_in
	]

	for i, f in enumerate((sol0, sol1)):
		res = f(tiles)
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
